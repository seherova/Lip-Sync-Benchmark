def filter_cherry_output(input_file, output_file):
    replacement_map = {
        'G': 'B',
        'H': 'C',
        'I': 'B',
        'J': 'B',
        'K': 'E'
        
    }
    with open(input_file, 'r', encoding='utf-8') as f_in, open(output_file, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            time, viseme = line.strip().split('\t')
            viseme = replacement_map.get(viseme, viseme)
            f_out.write(f"{time}\t{viseme}\n")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("python filter_cherry_output.py <input_dosyası> <çıktı_dosyası>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        filter_cherry_output(input_file, output_file)
