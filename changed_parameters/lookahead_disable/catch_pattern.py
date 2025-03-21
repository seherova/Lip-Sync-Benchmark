import os

# Fonem sözlüğü (örnek)
phoneme_dict = {
    'A': ['CC'],
    'E': ['CDB', 'DB'],
    'İ': ['BB', 'B'],
    'O': ['EC'],
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
    
    input_path = "/Users/seherova/Documents/projectss/speech-lip sync-sync/cherry-lip-sync/cherry-output/son_guncellemeler/changed_parameters/lookahead_disable/changed_test_sound.txt"
    

    data = []
 
    try:
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
    except Exception as e:
        print(f"Dosya okunurken hata oluştu: {e}")
        return

    final_output = []
    i = 0
    while i < len(data):
        time_i, shape_i = data[i]
        matched = False

        # Eğer token "X" ise direkt A (0) olarak ekle
        if shape_i == "X":
            final_output.append((time_i, 'A'))
            vowel_counts['A'] += 1
            global unmatched_count
            unmatched_count += 1
            i += 1
            continue

        # Diğer tokenlar için örüntüleri dene
        for vowel, pat in pattern_list:
            plen = len(pat)
            if i + plen <= len(data):
                seq = ''.join(data[j][1] for j in range(i, i + plen))
                if seq == pat:
                    last_time = data[i + plen - 1][0]
                    final_output.append((last_time, vowel))
                    vowel_counts[vowel] += 1
                    i += plen
                    matched = True
                    break

        # Hiçbir örüntü eşleşmezse, varsayılan A
        if not matched:
            final_output.append((time_i, 'A'))
            vowel_counts['A'] += 1
            unmatched_count += 1
            i += 1

    mapping = {'A': 0, 'E': 1, 'İ': 2, 'O': 3, 'U': 4}
    final_mapped = [(t, mapping[p]) for (t, p) in final_output]

    output_file = "/Users/seherova/Documents/projectss/speech-lip sync-sync/cherry-lip-sync/cherry-output/son_guncellemeler/changed_parameters/lookahead_disable/cached_pattern.txt"
    

    if not os.path.exists(output_file):
        with open(output_file, "w", encoding="utf-8") as f:
            pass

    try:
        with open(output_file, "w", encoding="utf-8") as outfile:
            for (t, ph) in final_mapped:
                outfile.write(f"{t:.3f}\t{ph}\n")
            outfile.write("\nFonem Eşleşme Sayıları:\n")
            for vowel in vowel_counts:
                outfile.write(f"{vowel}: {vowel_counts[vowel]}\n")
            outfile.write("\nEşlenmeyen Sayılar:\n")
            outfile.write(f"{unmatched_count}\n")
        print(f"Çıktı başarıyla kaydedildi: {output_file}")
    except Exception as e:
        print(f"Çıktı dosyasına yazılırken hata oluştu: {e}")

if __name__ == "__main__":
    main()
