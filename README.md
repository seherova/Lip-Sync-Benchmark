# Lip-Sync Benchmark

Bu proje, Tapir Lab.'ın dil bağımsız lip-sync yönteminin (extended LPC tabanlı) performansını, Cherry Lip-Sync yöntemiyle karşılaştırmak (benchmark yapmak) amacıyla geliştirilmiştir. Dev branch’te yer alan kodlar, hem mevcut yöntemin temel sinyal işleme ve istatistiksel adımlarını korur hem de bu çıktıları zaman uyumlu olarak karşılaştırmaya yönelik benchmark modüllerini içerir. Uzun vadede, elde edilen benchmark sonuçlarına dayanarak Tapir Lab.'ın Lip-Sync yönteminin yapay zeka destekli optimizasyonunu entegre etmek planlanmaktadır.

## Proje Amacı

- **Benchmark:**  
  - Cherry Lip-Sync ile Tapir Lab. Lip-Sync çıktılarının zamana göre fonemleri ifade eden ağız şekillerinin karşılaştırılması. Dudak senkronizasyonunun sağlanacağı ses kaydı için Lip Sync.'te öncelikle extended LPC yöntemi kullanılarak ses sinyalinden formant frekansları ve ilgili istatistiksel parametreler çıkarılır; bu veriler daha sonra, eğitim aşamasında elde edilen referans değerlerle karşılaştırılarak dudak hareketleri eşleştirilir. Frame_shapes.txt bu şekilde oluşur.
  - Cherry Lip Sync.'te ise bu fonemler (A,E,İ,O,U) tek tek verilir. Her fonem için oluşan pattern/patternler yakalanır ve bu patternler ilgili foneme karşılık gelir.
  - Çıkarılan bu örüntüler(patternler) asıl seste bulunur ve asıl seste bu patternler yerine ilgili fonemler yazılır.
  - Cherry Lip Sync'in çıktısı ve Tapir Lip Sync.'in çıktısı aynı çıktı formatına dönüştürülerek benchmark işlemi uygulanır.

- **Gelecek Hedef – AI Destekli Optimizasyon:**  
  - Mevcut extended LPC tabanlı formant çıkarım yönteminin yerini, yapay zeka destekli formant tahmini ile değiştirmeyi hedefleyerek, gürültü ve koartikülasyon gibi durumlarda doğruluğu artırmak.
