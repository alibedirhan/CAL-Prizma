# Prizma Optik Simulatörü

Türkçe arayüze sahip interaktif prizma optik simülatörü. Bu uygulama, ışığın prizmadan geçerken nasıl kırıldığını ve renklere ayrıldığını görselleştirmenizi sağlar.

## 🌈 Özellikler

- **Gerçek Zamanlı Simülasyon**: Prizma açısı ve geliş açısını değiştirerek anında sonuçları görün
- **Dispersiyon Analizi**: Farklı dalga boylarının nasıl farklı açılarda saptığını gözlemleyin
- **Fizik Hesaplamaları**: Snell yasası ve optik formüller görüntülenir
- **Görsel Sonuçlar**: Her rengin sapma açısı ve toplam dispersiyon değerleri
- **BK7 Cam**: Gerçek optik cam malzemesi özellikleri
- **Türkçe Arayüz**: Tamamen Türkçe kullanıcı arayüzü

## 📸 Ekran Görüntüleri

Simülatör aşağıdaki panelleri içerir:
- Prizma analizi ve ışın yolları
- Fizik hesaplamaları 
- Sapma açıları tablosu
- Dalga boyu - sapma açısı grafiği

## 🚀 Hızlı Başlangıç

### Windows Kullanıcıları (Exe Dosyası)

1. [Releases](../../releases) sayfasından en son `PrismSimulator.exe` dosyasını indirin
2. İndirilen dosyaya çift tıklayın
3. Simülatör otomatik olarak başlayacaktır

### Python ile Çalıştırma

#### Gereksinimler

```bash
pip install numpy matplotlib
```

#### Çalıştırma

```bash
python PrismSimulator.py
```

## 🎮 Kullanım

1. **Prizma Açısı**: Alt kısımdaki slider ile prizma açısını 30°-90° arası ayarlayın
2. **Geliş Açısı**: İkinci slider ile ışınların geliş açısını 15°-75° arası ayarlayın
3. **Sonuçları İzleyin**: 
   - Sol panel: Prizma ve ışın yolları
   - Orta paneller: Hesaplamalar ve sonuçlar
   - Sağ panel: Dispersiyon grafiği

## 🔬 Fizik Arka Planı

Bu simülatör aşağıdaki optik prensipleri kullanır:

- **Snell Yasası**: n₁sin(θ₁) = n₂sin(θ₂)
- **Prizma Sapma Formülü**: δ = i₁ + r₂ - A
- **Dispersiyon**: Farklı dalga boylarının farklı kırılma indisleri

### Kullanılan Değerler (Optik Cam)

| Renk | Dalga Boyu (nm) | Kırılma İndisi |
|------|----------------|----------------|
| Mor | 434 | 1.5270 |
| Mavi | 486 | 1.5230 |
| Yeşil | 510 | 1.5200 |
| Sarı | 546 | 1.5185 |
| Turuncu | 589 | 1.5170 |
| Kırmızı | 656 | 1.5145 |

## 🛠️ Geliştirme

### Kod Yapısı

```
PrismSimulator.py
├── SimplePrismSimulator (Ana sınıf)
├── __init__() - Başlangıç parametreleri
├── setup_interface() - Arayüz kurulumu
├── calculate_prism_ray_path() - Fizik hesaplamaları
├── draw_prism() - Prizma çizimi
├── draw_rays() - Işın yolları
└── update_simulation() - Gerçek zamanlı güncelleme
```



## 🙋‍♂️ SSS

**S: Tam iç yansıma ne demek?**
C: Işın prizmadan çıkamadığında oluşur. Geliş açısını azaltmayı deneyin.

**S: Dispersiyon neden oluşur?**
C: Farklı renklerin (dalga boylarının) farklı kırılma indisine sahip olması nedeniyle.

**S: Hangi açılarda en iyi dispersiyon görülür?**
C: Genelde 45-60° geliş açısı ve 60° prizma açısında iyi sonuçlar alınır.

## 📞 İletişim

Sorularınız için GitHub Issues kullanabilirsiniz.
