import sys
import define_encoding
import json
from get_data_from_json import get_data_from_json
from get_data_from_tsv import get_data_from_tsv
from create_table import create_table

if __name__ == '__main__':
    filename = sys.argv[1]
    encoding = define_encoding.define_encoding(filename)
    try:
        data = get_data_from_json(filename, encoding)
    except json.decoder.JSONDecodeError:
        data = get_data_from_tsv(filename, encoding)
    print(create_table(data))
