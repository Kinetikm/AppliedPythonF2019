import sys

# Ваши импорты
import json

if __name__ == '__main__':
    filename = sys.argv[1]

    # Ваш код
    with open(filename) as json_file:
        json_data = json.load(json_file)
        print(type(json_data))
        print(json_data)
        for row in json_data:
            print('{}\t{}\t{}'.format(row))
