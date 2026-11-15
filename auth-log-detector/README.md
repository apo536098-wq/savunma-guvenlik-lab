# Sentetik kimlik doğrulama log tespitçisi

Bu araç JSON Lines biçimindeki **sentetik** olayları okur ve aynı kaynak IP'den bir kayan pencere içinde belirlenen sayıda başarısız giriş olup olmadığını raporlar. Gerçek sunucu loglarını otomatik toplamaya/işlemeye göre tasarlanmamıştır; ağ erişimi, engelleme veya müdahale özelliği yoktur.

## Çalıştırma

```bash
python auth-log-detector/src/generate_sample.py
python auth-log-detector/src/detector.py auth-log-detector/data/sample_auth.jsonl --threshold 5 --window-seconds 60
python -m unittest discover -s auth-log-detector -p 'test_*.py'
```

Her satırda ISO-8601 `timestamp`, dokümantasyon amaçlı `source_ip` ve `result` (`failure` veya `success`) alanları bulunur. Zaman damgası UTC `Z` veya saat dilimi içermelidir. Varsayılan eşik 5 başarısız olay / 60 saniyedir. Çıktı bir inceleme uyarısıdır; tek başına saldırı kanıtı değildir. Gerçek kullanıcı verilerini depoya koymayın.
