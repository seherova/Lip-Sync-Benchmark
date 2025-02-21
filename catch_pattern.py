# cherry_phonemes_dictionary dosyasındaki fonem temsilleri (sabit olarak kod içerisine alındı)
# A: ECC, CC
# E: CDB, DB
# İ: B, BB
# O: EC
# U: CA
phoneme_dict = {
    'A': ['ECC', 'CC'], #'DC'
    'E': ['CDB', 'DB'], #CD
    'İ': ['BB', 'B'],
    'O': ['EC'],
    'U': ['CA']#CA manuel girildi
}

# Aday eşleşme yapılacak sembollerin başlangıç harflerini topluyoruz.
candidate_start_set = set()
for vowel, patterns in phoneme_dict.items():
    for pattern in patterns:
        candidate_start_set.add(pattern[0])

# Fonem eşleşme sayılarını tutacak sayaçlar
vowel_counts = {'A': 0, 'E': 0, 'İ': 0, 'O': 0, 'U': 0}
unmatched_count = 0  # eşleşmeyenlerin sayısı

def process_segment(segment_tokens):
    """
    X (sessizlik) dışındaki ardışık ağız şekillerinden oluşan listeyi,
    tanımlı fonem temsilleriyle eşleştirip, güncellenmiş çıktı listesi döner.
    """
    global unmatched_count
    output_tokens = []
    i = 0
    while i < len(segment_tokens):
        token = segment_tokens[i]
        # Eğer token, aday başlangıç harfleri arasında değilse, doğrudan ekle.
        if token not in candidate_start_set:
            output_tokens.append("(" + token + ")")
            unmatched_count += 1
            i += 1
        else:
            # Token ile başlayan tüm fonem temsili adaylarını topluyoruz.
            candidates = []
            for vowel, patterns in phoneme_dict.items():
                for pattern in patterns:
                    if pattern[0] == token:
                        candidates.append((vowel, pattern, len(pattern)))
            # En uzun temsili önce denemek için azalan sırada sıralıyoruz.
            candidates.sort(key=lambda x: x[2], reverse=True)
            matched = False
            for vowel, pattern, plen in candidates:
                if i + plen <= len(segment_tokens):
                    if ''.join(segment_tokens[i:i+plen]) == pattern:
                        # Eşleşme bulunduğunda, sadece ilgili ses ekleniyor (örn. "A")
                        output_tokens.append(vowel)
                        vowel_counts[vowel] += 1
                        i += plen  # Eşleşen uzunluk kadar atlıyoruz.
                        matched = True
                        break
            if not matched:
                # Uyuşan temsili bulunamazsa, token parantez içinde yazılır ve eşleşmeyen sayısı arttırılır.
                unmatched_count += 1
                output_tokens.append("(" + token + ")")
                i += 1
    return output_tokens

def main():
    final_output = []
    current_segment = []
    
    # output.txt dosyasını satır satır işliyoruz.
    # Her satırda ilk sütun zaman değeri, ikinci sütun ağız şeklidir.
    with open("/Users/seherova/Documents/projectss/speech-lip sync-sync/cherry-lip-sync/cherry-output/updated_output_voice.txt", "r", encoding="utf-8") as infile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            # Sadece ikinci sütun (ağız şekli) işleme alınacak.
            mouth_shape = parts[1]
            if mouth_shape == "X":
                # "X" sessizlik; segment varsa işlenip sonuç ekleniyor.
                if current_segment:
                    processed = process_segment(current_segment)
                    final_output.extend(processed)
                    current_segment = []
                # Sessizlik sembolü X, extract_output.txt’ye yazılmıyor.
            else:
                current_segment.append(mouth_shape)
    # Dosya sonuna gelince, kalan segment varsa işleyelim.
    if current_segment:
        processed = process_segment(current_segment)
        final_output.extend(processed)
    
    # extract_output.txt dosyasına, güncellenmiş ağız şekillerini satır satır yazıyoruz.
    # Fonem eşleşme sayılarını ve eşleşmeyen sayıların toplamını da ekliyoruz.
    with open("amy_extract_output.txt", "w", encoding="utf-8") as outfile:
        for token in final_output:
            outfile.write(token + "\n")
        outfile.write("\nFonem Eşleşme Sayıları:\n")
        for vowel in vowel_counts:
            outfile.write(f"{vowel}: {vowel_counts[vowel]}\n")
        outfile.write("\nEşlenmeyen Sayılar:\n")
        outfile.write(f"{unmatched_count}\n")

if __name__ == "__main__":
    main()
