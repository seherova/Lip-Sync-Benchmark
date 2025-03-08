import sys
import os

def extract_cherry_pattern(lines):
    segments = []
    current_segments = []
    first_x_found = False

    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        # Zaman değeri ve sembolü ayırıyoruz.
        time_value = parts[0]
        symbol = parts[1]

        if symbol == 'X':
            if not first_x_found:
                # İlk X'i başlangıç noktası olarak kabul et.
                first_x_found = True
                current_segments = []
            else:
                # Yeni bir X geldiğinde, toplanan harfleri bir segment olarak ekle.
                segment_str = ''.join(current_segments)
                if segment_str:  # Boş segmentleri eklemiyoruz.
                    segments.append(segment_str)
                current_segments = []
        else:
            # X olmayan semboller segmente eklenir.
            current_segments.append(symbol)
    return segments

def count_segments(segments):
    counts = {}
    for seg in segments:
        counts[seg] = counts.get(seg, 0) + 1
    return counts

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except Exception as e:
        print("Error reading file:", file_path, e)
        sys.exit(1)
        
    segments = extract_cherry_pattern(lines)
    counts = count_segments(segments)
    
    candidate_patterns = []
    if counts:
        max_counts = max(counts.values())
        for pattern, count in counts.items():
            if count == max_counts or count == max_counts - 1:
                candidate_patterns.append(pattern)
    return segments, counts, candidate_patterns

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_cherry_phonemes.py input1.txt input2.txt ...")
        sys.exit(1)
    
    phoneme_dictionary = {}
    
    # Her dosya için işlemleri yap:
    for file_path in sys.argv[1:]:
        # Dosya isminin uzantısız hali anahtar olarak kullanılacak.
        base = os.path.basename(file_path)
        phoneme_key = os.path.splitext(base)[0]
        
        segments, counts, candidate_patterns = process_file(file_path)
        
        print(f"\nDosya: {file_path}")
        if segments:
            print("Number of total segments:", len(segments))
            print("Segment patterns:", segments)
            print("Frequency of unique patterns:")
            for pattern, count in counts.items():
                print(f"{pattern}: {count} kez")
                
            if len(candidate_patterns) == 1:
                print("Bu fonemi temsil edebilecek ağız şekilleri örüntüsü:",
                      candidate_patterns[0], f"({counts[candidate_patterns[0]]} kez)")
                phoneme_dictionary[phoneme_key] = candidate_patterns[0]
            else:
                print("Fonemin olası ağız işareti örüntüleri:")
                for pattern in candidate_patterns:
                    print(f"{pattern} ({counts[pattern]} kez)")
                phoneme_dictionary[phoneme_key] = candidate_patterns
        else:
            print("Hiç segment bulunamadı.")
    
    # Sonuç sözlüğünü tek seferde dosyaya yazıyoruz.
    output_file = "extracted_pattern.txt"
    try:
        with open(output_file, 'w', encoding="utf-8") as out:
            out.write(str(phoneme_dictionary))
        print(f"\nFonem örüntü sözlüğü '{output_file}' dosyasına kaydedildi.")
    except Exception as e:
        print("Error writing to file:", e)

if __name__ == '__main__':
    main()
