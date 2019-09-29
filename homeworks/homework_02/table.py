import sys
from check_module import FileChecker, get_enc
from create_table import create_table, get_matrix

if __name__ == '__main__':
    filename = sys.argv[1]
    if FileChecker(filename):
        if not get_enc(filename):
            print("Формат не валиден")
        else:
            matr = get_matrix(filename)
            matrix = create_table(matr)
            for i in matrix:
                print(i)
