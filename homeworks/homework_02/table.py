import sys
from table_maker import make_table
from decoder import get_encoding
from reader import read_file


if __name__ == '__main__':
    filename = sys.argv[1]
    try:
        f = open(filename)
    except FileNotFoundError:
        print("Файл не валиден")
    else:
        f.close()
        enc_type = get_encoding(filename)
        if enc_type:
            data = read_file(filename, enc_type)
            if data:
                print(make_table(data))
            else:
                print("Формат не валиден")
        else:
            print("Формат не валиден")
