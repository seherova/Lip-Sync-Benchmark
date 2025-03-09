#!/usr/bin/env python3
import sys
import os

def process_file(filename):
    """
    Dosyayı okuyup, her satırı (zaman, harf) çiftlerine dönüştürür.
    'X' harfleri segment sınırlarını belirler.
    İki X arasındaki segmentte:
      - Eğer segmentte yalnız 1 veri varsa, bu veri ile sonraki X arasındaki zaman farkı hesaplanır.
      - Eğer segmentte 2 ya da daha fazla veri varsa, ardışık (overlapping) çiftler hesaplanır.
    Sonuç, geçiş etiketlerine göre (örn. "D-C", "D-B", "B", vb.) gruplanan zaman farklarıdır.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    data = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        time_str = parts[0].replace(',', '.')
        try:
            t = float(time_str)
        except ValueError:
            continue
        letter = parts[1].upper()
        data.append((t, letter))

    # 'X' harflerinin indekslerini tespit ediyoruz (segment sınırları)
    x_indices = [i for i, (_, l) in enumerate(data) if l == 'X']
    segments = []
    for i in range(len(x_indices) - 1):
        start_idx = x_indices[i]
        end_idx = x_indices[i + 1]
        # Segment: iki X arasındaki satırlar (sınırları hariç)
        segment = data[start_idx + 1:end_idx]
        segments.append({
            "start_time": data[start_idx][0],
            "end_time": data[end_idx][0],
            "data": segment
        })

    # Her segmentteki geçişleri hesaplıyoruz.
    transitions = []  # (geçiş etiketi, zaman farkı)
    for seg in segments:
        seg_data = seg["data"]
        if not seg_data:
            continue
        if len(seg_data) == 1:
            # Tek veri varsa; geçiş zamanı: sonraki X zamanı - bu veri zamanı.
            letter = seg_data[0][1]
            diff = seg["end_time"] - seg_data[0][0]
            transitions.append((letter, diff))
        else:
            # İki ya da daha fazla veri varsa, ardışık çiftler hesaplanıyor.
            for i in range(len(seg_data) - 1):
                label = f"{seg_data[i][1]}-{seg_data[i+1][1]}"
                diff = seg_data[i+1][0] - seg_data[i][0]
                transitions.append((label, diff))

    # Geçişleri etiketlerine göre gruplandıralım.
    groups = {}
    for label, diff in transitions:
        groups.setdefault(label, []).append(diff)
    return groups

def format_output(filename, groups):
    """
    Dosya adına (ilk harfine göre) ses türünü belirleyip,
    istenen formatta çıktı oluşturur.
    """
    base = os.path.basename(filename)
    vowel = base[0].upper()  # Örneğin "u.txt" -> 'U'
    output = ""
    
    if vowel == 'U':
        output += "Rhubarb'da U sesi oluşurken eşleşen ağız şekilleri:\n\n"
        if "D-C" in groups:
            output += "D-C\n"
            for i, diff in enumerate(groups["D-C"], start=1):
                output += f"{i}- {diff:.2f}\n"
            output += "\n"
        if "D-B" in groups:
            output += "D-B\n"
            for i, diff in enumerate(groups["D-B"], start=1):
                output += f"{i}- {diff:.2f}\n"
            output += "\n"
        if "B" in groups:
            output += "B\n"
            for i, diff in enumerate(groups["B"], start=1):
                output += f"{i}- {diff:.2f}\n"
            # Eğer B grubundan birden fazla değer varsa ortalamayı hesaplayıp özet satırı ekle.
            if len(groups["B"]) > 1:
                avg_B = sum(groups["B"]) / len(groups["B"])
                output += f"\nB ağız şeklinden sonra ortalama **{avg_B:.3f}** sn sonra gelen B ağız şekli {avg_B:.3f}'ı oluşturuyor.\n"
            output += "\n"
    
    elif vowel == 'O':
        if "C-B" in groups:
            output += "   C-B\n"
            for i, diff in enumerate(groups["C-B"], start=1):
                output += f"{i}- {diff:.2f}\n"
            avg = sum(groups["C-B"]) / len(groups["C-B"])
            output += f"\nortalama = {avg:.3f}\n\n"
            output += f"C ağzını ortalama **{avg:.3f}** sn süreyle B ağzı takip ediyorsa ses O sesidir.\n"
    
    elif vowel == 'I':
        output += "İ sesi için ağız şekilleri:\n\n"
        if "C-B" in groups:
            count = len(groups["C-B"])
            output += f"C-B ({count} tane C-B)\n\n"
            for diff in groups["C-B"]:
                output += f"C-B -> {diff:.2f}\n"
            output += "\n"
            if count > 1:
                avg_cb = sum(groups["C-B"]) / count
                output += f"C ağız şeklinden sonra ortalama **{avg_cb:.3f}** sn sonra gelen B ağız şekli {avg_cb:.3f}'ı oluşturuyor.\n\n"
        if "B-C" in groups:
            count = len(groups["B-C"])
            output += f"B-C ({count} tane B-C)\n\n"
            for diff in groups["B-C"]:
                output += f"B-C -> {diff:.2f}\n"
            output += "\n"
        if "B" in groups:
            count = len(groups["B"])
            output += f"B ({count} tane B)\n\n"
            for diff in groups["B"]:
                output += f"{diff:.2f}\n"
            output += "\n"
        if "D-B" in groups:
            count = len(groups["D-B"])
            output += f"D-B ({count} tane D-B)\n\n"
            for diff in groups["D-B"]:
                output += f"D-B -> {diff:.2f}\n"
            output += "\n"
    
    elif vowel == 'E':
        output += "Rhubarb'da E sesi x süre arayla art arda gelen C ve B seslerinden oluşur. Ortalama x süresi.\n\n"
        output += "C - B\n\n"
        if "C-B" in groups:
            for i, diff in enumerate(groups["C-B"], start=1):
                output += f"{i}- {diff:.2f}\n"
            avg = sum(groups["C-B"]) / len(groups["C-B"])
            output += f"\nortalama = {avg:.3f}\n\n"
            output += f"C ağız şeklinden sonra ortalama **{avg:.3f}** sn sonra gelen B ağız şekli {avg:.3f}'ı oluşturuyor.\n"
    
    elif vowel == 'A':
        output += ("A sesi Rhubarb'da C ve B seslerinin x sürede art arda gelmesiyle oluşur. "
                   "x süreyi bulmak için art arda çıkan 7 a harfinin ortalaması alınabilir.\n\n")
        output += "C ve B\n\n"
        if "C-B" in groups:
            for i, diff in enumerate(groups["C-B"], start=1):
                output += f"{i}- {diff:.2f}\n"
            avg = sum(groups["C-B"]) / len(groups["C-B"])
            diffs_str = " + ".join(f"{d:.2f}" for d in groups["C-B"])
            output += f"\nortalaması ({diffs_str}) / {len(groups['C-B'])} = {avg:.2f}\n"
    
    else:
        # Varsayılan biçimlendirme
        for label, diffs in groups.items():
            output += f"{label}:\n"
            for i, diff in enumerate(diffs, start=1):
                output += f"{i}- {diff:.2f}\n"
            output += "\n"
    return output

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <file1> <file2> ...")
        sys.exit(1)
    # Komut satırından verilen her dosya için işlemi yapıyoruz.
    for filename in sys.argv[1:]:
        if not os.path.exists(filename):
            print(f"File {filename} does not exist.")
            continue
        groups = process_file(filename)
        output = format_output(filename, groups)
        print(f"== Output for {filename} ==")
        print(output)
        print("\n" + "="*40 + "\n")

if __name__ == "__main__":
    main()
