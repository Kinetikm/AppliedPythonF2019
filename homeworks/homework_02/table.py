import sys

from homeworks.homework_02.table.reader import TableReader
from homeworks.homework_02.table.parser import parse_table
from homeworks.homework_02.table.dumper import dump_table

if __name__ == '__main__':

    if len(sys.argv) < 2:
        sys.exit(0)

    # Ваш код
    treader = TableReader(sys.argv[1])
    data = None
    try:
        data = treader.read()
    except FileNotFoundError:
        print("Файл не валиден")
        sys.exit(1)
    except ValueError:
        print("Формат не валиден")
        sys.exit(1)

    parsed_table = parse_table(data)
    if parsed_table is None:
        print("Cant parse table! In file:", treader.filename)
        sys.exit(1)

    dump_table(parsed_table)
