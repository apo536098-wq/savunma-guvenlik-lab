# Parola entropisi ve hash maliyeti karşılaştırması

Yalnızca kod içindeki sentetik örnekleri kullanır; parola girişi istemez, ağa bağlanmaz ve parola tahmin etmez. MD5/SHA-256 bölümü, parola saklama için neden uygun olmadıklarını göstermek amacıyla **hız karşılaştırması** yapar. scrypt, standart kütüphanedeki bellek maliyetli parola türetme örneğidir.

> Eğitim ölçümü donanıma ve Python/OpenSSL derlemesine göre değişir; güvenlik parametresi önerisi veya üretim kıyaslaması değildir. Üretimde platformunuzun güncel parola-hash kütüphanesini ve rehberliğini kullanın.

## Çalıştırma

```bash
python password-analysis/src/password_metrics.py
python -m unittest discover -s password-analysis -p 'test_*.py'
```

Program parolaları değil yalnızca uzunluk, entropi tahmini (bit), algoritma adı ve geçen süreyi yazdırır. Karakter kümesi entropisi, gerçek parolanın rastgele üretildiğini varsaydığı için insanın seçtiği parolaların gerçek gücünü abartabilir.
