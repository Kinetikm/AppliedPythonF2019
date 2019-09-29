import sys
import json
import os
import traceback
from json_handler import JSONHandler
from tsv_handler import TSVHandler
from pretty_print import PrettyPrint


if __name__ == '__main__':
    filename = sys.argv[1]
    encoding_list = ['utf-8', 'utf-16', 'cp1251']
    try:
        with open(filename, 'rb') as f:
            bytes_ = f.read()
    except FileNotFoundError:
        print('Файл не валиден')
    for coding in encoding_list:
        try:
            text = bytes_.decode(coding)
            break
        except UnicodeDecodeError:
            continue
    try:
        struct = json.loads(text)
        handler = JSONHandler()
    except json.decoder.JSONDecodeError:
        struct = [line.strip().split('\t') for line in text.split('\n') if line]
        handler = TSVHandler()
    except Exception:
        print(traceback.format_exc())
    finally:
        cur = sys.modules[__name__]
        if hasattr(cur, 'handler'):
            pretty_printer = PrettyPrint(handler, struct)
            pretty_printer.pretty_print()
