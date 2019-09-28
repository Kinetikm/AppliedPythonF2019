import sys

from file_actions import get_encoding_file, get_data_from_file
from formatting import transform_to_schema
from exceptions import ValidDataException


if __name__ == "__main__":
    filename = sys.argv[1]

try:
    data = get_data_from_file(filename)
    print(transform_to_schema(data))
except ValidDataException:
    print("Формат не валиден")
except FileNotFoundError:
    print("Файл не валиден")
