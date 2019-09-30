import sys

# Ваши импорты
from ChooseOfEncode import *
from ChooseOfType import *
from PrintInConsole import *

if __name__ == '__main__':
    filename = sys.argv[1]

    # Ваш код
    try:
        input_data = choose_of_encode(filename)
        input_data = choose_type(input_data)
        pretty_print_table(input_data)
    except FileNotFoundError:
        print("Файл не валиден")
    except UnicodeDecodeError:
        print("Формат не валиден")
    except:
        print("Формат не валиден")
