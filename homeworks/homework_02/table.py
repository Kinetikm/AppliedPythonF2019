import sys

import myFileOpen
import myUnpack
import myPrint

if __name__ == '__main__':
    filename = sys.argv[1]

    txt, err = myFileOpen.fopen(filename)
    # if err == 1:
    #     print("Файл не валиден")
    #     exit(0)
    # elif err == 2:
    #     print("Формат не валиден")
    #     exit(0)

    tbl = myUnpack.unpack(txt)
    if tbl is None:
        print("Формат не валиден")
        exit(0)

    myPrint.print_table(tbl)
