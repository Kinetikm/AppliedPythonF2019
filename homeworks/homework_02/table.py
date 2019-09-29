import sys

import homeworks.homework_02.table_util.encoder as encoder
import homeworks.homework_02.table_util.parser as parser
import homeworks.homework_02.table_util.viewer as viewer


if __name__ == '__main__':
    filename = sys.argv[1]
    encoded_data = encoder.encode_file(filename)
    if encoded_data is None:
        exit(1)
    parsed_data = parser.parse_data(encoded_data)
    if parsed_data is None:
        exit(1)
    viewer.print_view(parsed_data)
