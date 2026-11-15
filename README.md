# Savunma Güvenlik Laboratuvarı

Yasal, yerel ve savunma odaklı mini projeler: tersine mühendislik temelleri, parola saklama güvenliği ve kimlik doğrulama günlüklerinde anomali tespiti.

> **Güvenlik sınırı:** Bu depo yalnızca sizin oluşturduğunuz örnek dosyaları ve sentetik günlükleri işler. Ağ bağlantısı kurmaz, parola tahmini yapmaz, sistemleri taramaz veya otomatik engelleme uygulamaz. `crackme` bilerek basit bir eğitim örneğidir; gerçek ürünlerde sabit gömülü sırlar kullanılmamalıdır.

## Projeler

1. **`crackme/` — Yerel CrackMe ve ELF/PE başlık inceleyicisi**  
   Küçük C örneğini kendiniz derleyip dosya biçimi başlıklarını ve basılabilir dizgileri inceleyin. Analyzer dosyayı çalıştırmaz.
2. **`password-analysis/` — Parola entropisi ve hash maliyeti**  
   Sentetik parolalar için basit entropi tahmini ve MD5/SHA-256 ile bellek-maliyetli scrypt karşılaştırması. Gerçek parola girmeyin. Bu bir parola kırma aracı değildir.
3. **`auth-log-detector/` — Sentetik kimlik doğrulama günlüklerinde tespit**  
   JSONL örnek olaylar içinde belirli zaman penceresindeki başarısız giriş yoğunluğunu bulur. IP'leri engellemez ve hiçbir sisteme bağlanmaz.

## Hızlı başlangıç

Python 3.10+ ve (yalnızca ilk proje için) bir C derleyicisi gerekir. Projeler standart kütüphaneyi kullanır; üçüncü taraf Python paketi gerekmez.

```bash
python -m unittest discover -s . -p 'test_*.py'
python password-analysis/src/password_metrics.py
python auth-log-detector/src/generate_sample.py
python auth-log-detector/src/detector.py auth-log-detector/data/sample_auth.jsonl
```

CrackMe'yi derleme ve inceleme yönergeleri `crackme/README.md` içindedir. Derlenen dosyalar yerel çalışma çıktısıdır, depoya eklenmez.

## Etik ve güvenli kullanım

- Yalnızca bu depodaki örnekler veya açıkça izinli yerel eğitim dosyaları üzerinde çalışın.
- Hassas parola, erişim anahtarı, gerçek kullanıcı günlüğü ya da kişisel veri commit etmeyin.
- Güvenlik olayları için tespit çıktısını inceleme sinyali olarak kullanın; tek başına otomatik karar değildir.
- Üretim sistemleri için güncel, denetlenmiş parola saklama kütüphaneleri ve yapılandırmaları kullanın.

## Öğrenme hedefleri

ELF/PE tanımlayıcıları, derleyici çıktısındaki dizgiler, entropi tahmininin sınırlılıkları, yavaş ve tuzlu parola türetme işlevleri, kayan zaman penceresi ve sentetik verilerle tespit testi.

## Lisans

MIT. Ayrıntılar için `LICENSE` dosyasına bakın.
