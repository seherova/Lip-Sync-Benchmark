"""
    * Bu algoritma sayesinde, girişteki zaman damgalı ağız şekli verilerinden önceden belirlenen fonem
    örüntüleri aranır, tespit edilen örüntüler ilgili fonemlere dönüştürülür ve sonuçlar istatistiksel
    bilgilerle birlikte çıktı dosyasına kaydedilir. *
    
    Kod, bir girdi dosyasındaki zaman damgası ve ağız şekli bilgilerini okur.
    Her token için, tanımlı fonem örüntülerinin sıralı kontrolü yapılır; eşleşme bulunduğunda ilgili sesli harf belirlenir.
    
    Örüntü Eşleştirme:
       1-  Token "X" (sessizlik) ise doğrudan varsayılan "A" seçilir. (Karşılaştırmanın yapılacağı Lip.  Sync. kodunda da sessizlik A(0) şeklinde alındığı için burada da sessizliği A(0) şeklinde alıyoruz.)
       2-  Diğer token dizileri için, önceden tanımlı fonem örüntüleri (örn. "ECC", "CC" vb.) en uzun örüntü önce denenecek şekilde sıralanır.
       3-  Eğer token dizisi tanımlı bir örüntüyle eşleşirse, o örüntüye karşılık gelen sesli harf belirlenir.
       4-  Hiçbir örüntü eşleşmezse yine varsayılan "A" seçilir.
    Çıktı Oluşturma:
           Elde edilen fonemler, A, E, İ, O, U olarak kalır; daha sonra bunlar sırasıyla 0, 1, 2, 3, 4 sayısal kodlarına dönüştürülür.
"""

import os

# Fonem sözlüğü (örnek)
phoneme_dict = {
        'A': ['CC'],
        'E': ['DB'],
        'İ': ['BA'],
        'O': ['ECECA', 'ECEA', 'ECA', 'EA'],
        'U': ['CA']
    }


# Tüm örüntüleri (fonem, pattern) listesi olarak derleyelim
pattern_list = []
for vowel, patterns in phoneme_dict.items():
    for pat in patterns:
        pattern_list.append((vowel, pat))

# En uzun örüntü önce denensin
pattern_list.sort(key=lambda x: len(x[1]), reverse=True)

vowel_counts = {'A': 0, 'E': 0, 'İ': 0, 'O': 0, 'U': 0}
unmatched_count = 0

def main():
    # Girdi dosyası
    input_path = "/Users/seherova/Documents/fonemlerveses/changed_dropout_parameter/updated_test_sound_dropout.txt"
    data = []

    # 1) Dosyayı okuyalım
    with open(input_path, "r", encoding="utf-8") as infile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            try:
                ts = float(parts[0])
            except ValueError:
                continue
            shape = parts[1]
            data.append((ts, shape))

    final_output = []
    i = 0
    while i < len(data):
        time_i, shape_i = data[i]
        matched = False

        # 2) Eğer X ise, doğrudan A (0) olarak çıktı ekledik
        if shape_i == "X":
            final_output.append((time_i, 'A'))
            vowel_counts['A'] += 1
            global unmatched_count
            unmatched_count += 1
            i += 1
            continue

        # 3) X değ ilse, örüntüleri dene
        for vowel, pat in pattern_list:
            plen = len(pat)
            if i + plen <= len(data):
                # i'den i+plen'e kadar tokenları birleştir
                seq = ''.join(data[j][1] for j in range(i, i + plen))
                if seq == pat:
                    # Eşleştiyse, tek satır çıktı (son token'ın zaman damgası)
                    last_time = data[i + plen - 1][0]
                    final_output.append((last_time, vowel))
                    vowel_counts[vowel] += 1
                    i += plen
                    matched = True
                    break

        # Hiçbir örüntü eşleşmediyse, varsayılan A
        if not matched:
            final_output.append((time_i, 'A'))
            vowel_counts['A'] += 1
            unmatched_count += 1
            i += 1

   
    mapping = {'A': 0, 'E': 1, 'İ': 2, 'O': 3, 'U': 4}
    final_mapped = [(t, mapping[p]) for (t, p) in final_output]

 
    #script_dir = os.path.dirname(os.path.abspath(__file__))
    #output_file = os.path.join(script_dir, "catched_pattern.txt")
    output_file = "/Users/seherova/Documents/fonemlerveses/changed_dropout_parameter/ch_dropout_catched_pattern_txt"


    with open(output_file, "w", encoding="utf-8") as outfile:
        for (t, ph) in final_mapped:
            outfile.write(f"{t:.3f}\t{ph}\n")
        outfile.write("\nFonem Eşleşme Sayıları:\n")
        for vowel in vowel_counts:
            outfile.write(f"{vowel}: {vowel_counts[vowel]}\n")
        outfile.write("\nEşlenmeyen Sayılar:\n")
        outfile.write(f"{unmatched_count}\n")

if __name__ == "__main__":
    main()
