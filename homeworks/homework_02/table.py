import sys
import define_encoding
import json
import process_tsv
from process_json import process_json
from draw_table import draw_table

if __name__ == '__main__':
    filename = sys.argv[1]
    encoding = define_encoding.define_encoding(filename)
    is_json = False
    try:
        data = process_json(filename, encoding)
        is_json = True
    except json.decoder.JSONDecodeError:
        pass
    if not is_json:
        try:
            data = process_tsv.process_tsv(filename, encoding)
        except FormatError as e:
            print(e)
    draw_table(data)
