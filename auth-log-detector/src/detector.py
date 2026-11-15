#!/usr/bin/env python3
"""Sentetik JSONL kimlik doğrulama olaylarında kayan pencere tespiti."""
from __future__ import annotations

import argparse
import ipaddress
import json
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path


def parse_timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp saat dilimi içermeli (ör. UTC Z)")
    return parsed.astimezone(timezone.utc)


def detect(path: Path, threshold: int = 5, window_seconds: int = 60) -> list[dict]:
    if threshold < 1 or window_seconds < 1:
        raise ValueError("threshold ve window_seconds pozitif olmalı")
    by_ip: dict[str, list[datetime]] = defaultdict(list)
    with path.open(encoding="utf-8") as source:
        for line_number, line in enumerate(source, start=1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
                address = ipaddress.ip_address(event["source_ip"])
                result = event["result"]
                timestamp = parse_timestamp(event["timestamp"])
            except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
                raise ValueError(f"Satır {line_number}: geçersiz olay ({exc})") from exc
            if result not in ("failure", "success"):
                raise ValueError(f"Satır {line_number}: result failure veya success olmalı")
            if result == "failure":
                by_ip[str(address)].append(timestamp)

    alerts = []
    window = window_seconds
    for address, timestamps in sorted(by_ip.items()):
        ordered = sorted(timestamps)
        active: deque[datetime] = deque()
        for current in ordered:
            active.append(current)
            while (current - active[0]).total_seconds() > window:
                active.popleft()
            if len(active) >= threshold:
                alerts.append({
                    "source_ip": address,
                    "attempt_count": len(active),
                    "window_start": active[0].isoformat(),
                    "window_end": current.isoformat(),
                    "window_seconds": window_seconds,
                })
                break
    return alerts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="Sentetik JSONL olay dosyası")
    parser.add_argument("--threshold", type=int, default=5)
    parser.add_argument("--window-seconds", type=int, default=60)
    args = parser.parse_args()
    try:
        alerts = detect(args.file, args.threshold, args.window_seconds)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps({"alerts": alerts, "alert_count": len(alerts)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
