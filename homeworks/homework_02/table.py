import json


# Ваши импорты


from convertings import json_to_table, tsv_to_table
from checkers import is_json, is_tsv, encoding_check, is_file_valid


# Ваш код
if __name__ == '__main__':
    to_out = ""
    f = is_file_valid()
    if f is not False:
        enc = encoding_check(f)
        if enc is not False:
            if is_json(f, enc) or is_tsv(f, enc):
                o = []
                if is_json(f, enc):
                    json_to_table(json.load(open(f, encoding=enc)), o)
                elif is_tsv(f, enc):
                    tsv_to_table(f, enc, o)
                for line in o:
                    print(line)
            else:
                print('Формат не валиден')
        else:
            print('Формат не валиден')
    else:
        print('Файл не валиден')
else:
    print('Файл не валиден')
