import sys

# Ваши импорты
from print_x import *
from homeworks.homework_02.encode_x import *
from type_x import *


if __name__ == '__main__':
    filename = sys.argv[1]

    # Ваш код
try:
    input_data = ch(filename)  # функция ch пытается открытть файл в различных кодировках
    input_data = type_x(input_data)
    print_x(input_data)
except FileNotFoundError:
        print("Файл не валиден")
except UnicodeDecodeError:
        print("Файл не валиден")
else:
        print("Формат не валиден")
