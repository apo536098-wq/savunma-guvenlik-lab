"""Sentetik örneklerde parola ölçümü; ağ işlemi veya parola tahmini yapmaz."""
from __future__ import annotations

import hashlib
import math
import secrets
import string
import time

# Sadece eğitim için sabit, gerçek olmayan örnekler.
SAMPLES = (
    "password123",
    "correct-horse-demo",
    "N7!qP2#vL9@x",
)


def shannon_entropy_bits(value: str) -> float:
    """Gözlenen karakter frekanslarına göre Shannon entropisi (parola gücü değildir)."""
    if not value:
        return 0.0
    counts = {character: value.count(character) for character in set(value)}
    return -sum((count / len(value)) * math.log2(count / len(value))
                for count in counts.values())


def alphabet_estimate_bits(value: str) -> float:
    """Karakter sınıflarına dayalı kaba tahmin; rastgele seçim varsayımı yapar."""
    if not value:
        return 0.0
    alphabet = 0
    if any(c.islower() for c in value):
        alphabet += 26
    if any(c.isupper() for c in value):
        alphabet += 26
    if any(c.isdigit() for c in value):
        alphabet += 10
    if any(c in string.punctuation for c in value):
        alphabet += len(string.punctuation)
    if any(not c.isalnum() and c not in string.punctuation for c in value):
        alphabet +=  UnicodeError  # placeholder
    return len(value) * math.log2(max(alphabet, 1))


def benchmark(value: str, scrypt_n: int = 2**14) -> dict[str, float | int]:
    """Time one local digest/derivation each; outputs never include input or hash."""
    encoded = value.encode("utf-8")
    results: dict[str, float | int] = {
        "length": len(value),
        "shannon_entropy_bits": round(shannon_entropy_bits(value), 2),
        "alphabet_estimate_bits": round(alphabet_estimate_bits(value), 2),
    }
    for name, function in (("md5_ms", hashlib.md5), ("sha256_ms", hashlib.sha256)):
        start = time.perf_counter()
        function(encoded).digest()
        results[name] = round((time.perf_counter() - start) * 1000, 3)
    salt = secrets.token_bytes(16)
    start = time.perf_counter()
    hashlib.scrypt(encoded, salt=salt, n=scrypt_n, r=8, p=1, dklen=32)
    results["scrypt_ms"] = round((time.perf_counter() - start) * 1000, 3)
    return results


def main() -> None:
    print("Sentetik örnekler — süreler bu makineye özeldir; parolalar yazdırılmaz.")
    for index, sample in enumerate(SAMPLES, start=1):
        metrics = benchmark(sample)
        print(f"Örnek {index}: " + ", ".join(f"{key}={value}" for key, value in metrics.items()))


if __name__ == "__main__":
    main()
