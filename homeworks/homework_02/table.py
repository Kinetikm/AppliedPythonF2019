import sys
# from homeworks.homework_02.read_file import read_file
# from homeworks.homework_02.draw_table import draw_table
# from homeworks.homework_02.encoding import ENCODINGS, get_encoding
from read_file import read_file
from draw_table import get_table
from encoding import ENCODINGS, get_encoding

if __name__ == '__main__':
    filename = sys.argv[1]
    # filename = "/Users/mac/PythonMail2019/AppliedPythonF2019/homeworks/homework_02/files/posts-utf8.tsv"
    try:
        f = open(filename)
    except FileNotFoundError:
        print("Файл не валиден")
    else:
        f.close()
        encoding = get_encoding(filename)
        if encoding in ENCODINGS:
            data = read_file(filename, encoding)
            if data:
                print(get_table(data))
            else:
                print("Формат не валиден")
        else:
            print("Формат не валиден")
