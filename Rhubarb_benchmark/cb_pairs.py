#!/usr/bin/env python3
import sys
import re

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py input.txt")
        sys.exit(1)
    
    filename = sys.argv[1]
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Düzenli ifade: Satırın başında sayısal değer (nokta veya virgül içerebilir),
    # ardından bir veya daha fazla boşluk ve ikinci sütun (ağız şekli harfi)
    pattern = re.compile(r'^\s*[\d\.,]+\s+(\S+)')
    
    mouth_shapes = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        m = pattern.match(line)
        if m:
            letter = m.group(1).upper()  # harfi büyük yapalım
            mouth_shapes.append(letter)
        else:
            # Eğer regex eşleşmezse, boşluklarla ayırıp ikinci sütunu alalım.
            parts = line.split()
            if len(parts) >= 2:
                letter = parts[1].strip().upper()
                mouth_shapes.append(letter)
    
    total = len(mouth_shapes)
    total_pairs = total - 1  # ardışık çift sayısı
    count_cb = 0
    for i in range(total_pairs):
        if mouth_shapes[i] == 'C' and mouth_shapes[i+1] == 'B':
            count_cb += 1
    
    probability = count_cb / total_pairs if total_pairs > 0 else 0
    
    print("Toplam ağız şekli sayısı:", total)
    print("Toplam ardışık çift sayısı:", total_pairs)
    print("C-B çiftlerinin sayısı:", count_cb)
    print("Tüm ardışık ağız şekilleri arasında C'den sonra B gelme olasılığı: {:.4f} (yani %{:.2f})".format(probability, probability*100))

if __name__ == "__main__":
    main()
