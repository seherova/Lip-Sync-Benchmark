# Lip-Sync Benchmark

Bu proje, Tapir Lab.'ın dil bağımsız lip-sync yönteminin (extended LPC tabanlı) performansını, Cherry Lip-Sync yöntemiyle karşılaştırmak (benchmark yapmak) amacıyla geliştirilmiştir. Dev branch’te yer alan kodlar, hem mevcut yöntemin temel sinyal işleme ve istatistiksel adımlarını korur hem de bu çıktıları zaman uyumlu olarak karşılaştırmaya yönelik benchmark modüllerini içerir. Uzun vadede, elde edilen benchmark sonuçlarına dayanarak Tapir Lab.'ın Lip-Sync yönteminin yapay zeka destekli optimizasyonunu entegre etmek planlanmaktadır.

## Proje Amacı

- **Benchmark:**  
  - Cherry Lip-Sync ile Tapir Lab.'ın Lip-Sync çıktılarının zamana göre fonem etiketlerinin karşılaştırılması.

- **Gelecek Hedef – AI Destekli Optimizasyon:**  
  - Mevcut extended LPC tabanlı formant çıkarım yönteminin yerini, yapay zeka destekli formant tahmini ile değiştirmeyi hedefleyerek, gürültü ve koartikülasyon gibi durumlarda doğruluğu artırmak.

## Kurulum

1. **Gereksinimler:**  
   - Python 3.x  
   - NumPy, OpenCV, librosa  
   - PyTorch (gelecekte AI modülü için kullanılacak)  
   - ffmpeg

2. **Bağımlılıkları Yükleyin:**

   ```bash
   pip install -r requirements.txt
