#!/usr/bin/env python3
"""Yerel eğitim binary'si için sınırlı ELF/PE metadata ve dizgi inceleyicisi.

Dosyayı çalıştırmaz; en fazla 16 MiB okur. Üçüncü taraf bağımlılığı yoktur.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

MAX_FILE_SIZE = 16 * 1024 * 1024
MACHINE_NAMES = {
    0x014C: "x86", 0x8664: "x86-64", 0x01C0: "ARM",
    0x01C4: "ARMv7", 0xAA64: "ARM64",
}


def printable_strings(data: bytes, min_length: int = 4) -> list[str]:
    """ASCII printable runs; does not decode or execute file contents."""
    found = re.findall(rb"[\x20-\x7e]{%d,}" % min_length, data)
    return [chunk.decode("ascii", errors="replace") for chunk in found[:100]]


def inspect_elf(data: bytes) -> dict:
    if len(data) < 16 or data[:4] != b"\x7fELF":
        raise ValueError("Geçerli ELF tanımlayıcısı bulunamadı")
    elf_class, encoding = data[4], data[5]
    if elf_class not in (1, 2) or encoding not in (1, 2):
        raise ValueError("Desteklenmeyen ELF class veya byte order")
    endian = "little" if encoding == 1 else "big"
    header_size = 52 if elf_class == 1 else 64
    if len(data) < header_size:
        raise ValueError("ELF başlığı eksik")
    machine = int.from_bytes(data[18:20], endian)
    entry_offset, entry_width = (24, 4) if elf_class == 1 else (24, 8)
    entry = int.from_bytes(data[entry_offset:entry_offset + entry_width], endian)
    return {
        "format": "ELF", "class": 32 if elf_class == 1 else 64,
        "byte_order": endian, "machine_id": machine,
        "entry_point": entry,
    }


def inspect_pe(data: bytes) -> dict:
    if len(data) < 0x40 or data[:2] != b"MZ":
        raise ValueError("Geçerli PE/DOS tanımlayıcısı bulunamadı")
    pe_offset = int.from_bytes(data[0x3C:0x40], "little")
    if pe_offset < 0x40 or pe_offset + 24 > len(data):
        raise ValueError("PE başlık konumu dosya sınırlarının dışında")
    if data[pe_offset:pe_offset + 4] != b"PE\0\0":
        raise ValueError("PE imzası bulunamadı")
    coff = data[pe_offset + 4:pe_offset + 24]
    machine = int.from_bytes(coff[0:2], "little")
    sections = int.from_bytes(coff[2:4], "little")
    optional_size = int.from_bytes(coff[16:18], "little")
    return {
        "format": "PE", "machine_id": machine, "section_count": sections,
        "optional_header_size": optional_size,
    }


def inspect(path: Path) -> dict:
    size = path.stat().st_size
    if size > MAX_FILE_SIZE:
        raise ValueError(f"Dosya {MAX_FILE_SIZE} bayt sınırını aşıyor")
    data = path.read_bytes()
    if data.startswith(b"\x7fELF"):
        result = inspect_elf(data)
    elif data.startswith(b"MZ"):
        result = inspect_pe(data)
    else:
        raise ValueError("Desteklenen ELF veya PE biçimi değil")
    result["file_size"] = size
    result["machine"] = MACHINE_NAMES.get(result["machine_id"], "bilinmeyen")
    result["printable_strings"] = printable_strings(data)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="İncelenecek yerel ELF/PE dosyası")
    args = parser.parse_args()
    try:
        print(json.dumps(inspect(args.file), indent=2, ensure_ascii=False))
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
