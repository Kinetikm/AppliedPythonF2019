from read_file import *
from draw_table import draw_table

# Ваши импорты


if __name__ == '__main__':
if __name__ == '__main__':
    filename = sys.argv[1]
    filename = sys.argv[1]

    list = read_file(filename)
    # Ваш код
    if list is not None:
        print(draw_table(list))
