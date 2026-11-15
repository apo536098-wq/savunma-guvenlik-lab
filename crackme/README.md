# CrackMe ve ELF/PE Analyzer

Bu laboratuvar, **kendinizin derlediği** basit bir C programını incelemek içindir. `analyze_binary.py` ELF/PE başlıklarından sınırlı metadata ve basılabilir dizgiler raporlar; dosyayı hiçbir zaman çalıştırmaz. Yalnızca güvendiğiniz, yerel eğitim dosyalarını analiz edin.

## Derle ve çalıştır (isteğe bağlı)

Linux/macOS ve GCC/Clang:

```bash
cc -O0 -g src/simple_license_checker.c -o crackme-demo
./crackme-demo
python src/analyze_binary.py crackme-demo
```

Windows'ta MinGW ile PE üretmek için:

```bash
gcc -O0 src/simple_license_checker.c -o crackme-demo.exe
python src/analyze_binary.py crackme-demo.exe
```

İsterseniz farklı optimizasyonlarla `-O0` ve `-O2` çıktılarının başlık/dizgi farklarını karşılaştırın. Assembly çalıştırmak gerekmez; derleyici çıktısını görmek için `cc -S -O0 src/simple_license_checker.c -o checker.s` kullanabilirsiniz.

## Öğrenme ve sınırlar

- ELF sınıfı, byte order, makine türü ve giriş noktası; PE makine türü ve bölüm sayısı gibi temel alanlar.
- ASCII basılabilir dizgilerin bir binary içinde bulunabilmesi.
- Eğitim örneğindeki sabit lisans metninin binary'de gizli olmadığı. Bu **gerçek lisanslama tasarımı değildir**.
- Analyzer header alanlarını güvenilmeyen girdi sayar, dosya boyutunu sınırlar ve dosyayı çalıştırmaz.

```bash
python -m unittest discover -s crackme -p 'test_*.py'
```
