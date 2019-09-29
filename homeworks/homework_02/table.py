import sys
import os

# Ваши импорты
from encodingsfilereader import EncodingsFileReader
from formats_parser import FormatReader
from pretty_formatter import PrettyFormatter
from exceptions import FileNotFound, InvalidFormat


if __name__ == '__main__':
    #os.environ["PYTHONIOENCODING"] = "utf-8"
    filename = sys.argv[1]
    try:
        sys.setdefaultencoding('utf-8')
    except AttributeError:
        pass

    try:
        open_result = EncodingsFileReader(filename)
        table = FormatReader(open_result.output_string)
        printer = PrettyFormatter(table.table, open_result.encoding)
        printer.print_whole()
    except (FileNotFound, InvalidFormat) as e:
        print(e)
