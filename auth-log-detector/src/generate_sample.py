#!/usr/bin/env python3
"""Tekrarlanabilir, sentetik auth olayları oluşturur; gerçek log kullanmaz."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


def sample_events() -> list[dict[str, str]]:
    start = datetime(2026, 1, 12, 10, 0, 0, tzinfo=timezone.utc)
    events = []
    for offset in range(6):
        events.append({
            "timestamp": (start + timedelta(seconds=offset * 5)).isoformat(),
            "source_ip": "192.0.2.10", "result": "failure",
        })
    events.extend([
        {"timestamp": (start + timedelta(minutes=2)).isoformat(),
         "source_ip": "198.51.100.23", "result": "failure"},
        {"timestamp": (start + timedelta(minutes=2, seconds=4)).isoformat(),
         "source_ip": "198.51.100.23", "result": "success"},
    ])
    return events


def main() -> None:
    output = Path(__file__).resolve().parents[1] / "data" / "sample_auth.jsonl"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("".join(json.dumps(event) + "\n" for event in sample_events()), encoding="utf-8")
    print(f"Sentetik örnek yazıldı: {output}")


if __name__ == "__main__":
    main()
