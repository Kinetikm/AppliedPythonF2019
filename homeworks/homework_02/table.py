from reading import *
from printing import *
import sys
import json


def main(filename):
    data = read_file(filename)
    if data:
        pretty_print(data)


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
        main(filename)
    except IndexError:
        print('Файл не валиден')
