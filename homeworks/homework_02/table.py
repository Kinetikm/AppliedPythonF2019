import sys
from read_format import check_enc, check_format
from draw_table import draw_table
from tsv_valid import is_tsv_valid

# Ваши импорты

if __name__ == '__main__':
    filename = sys.argv[1]

    # Ваш код
data = check_enc(filename)
if data is not None:
    data = check_format(data)
    if data[0] == "json":
        new_data = data[1]
        keys = new_data[0].keys()
        text = ["\t".join(keys)]
        for n in new_data:
            line = []
            for k in keys:
                line.append(str(n[k]))
            text.append("\t".join(line))
        draw_table(text)
    if data[0] == "tsv":
        text = data[1][:-1]
        if is_tsv_valid(text):
            draw_table(text)
        else:
            print("Формат не валиден")
