import sys
import json
import traceback
import json_handler
import tsv_handler
import pretty_print


if __name__ == '__main__':
    filename = sys.argv[1]

    encoding_list = ['utf-8', 'utf-16', 'cp1251']

    try:
        with open(filename, 'rb') as file:
            flow_bytes = file.read()
    except FileNotFoundError:
        print(traceback.format_exc())

    for encode in encoding_list:
        try:
            flow_symbol = flow_bytes.decode(encode)
            break
        except UnicodeDecodeError:
            continue

    try:
        packet = json.loads(flow_symbol)
        handler = json_handler.JSONHandler(packet)

    except json.decoder.JSONDecodeError:
        packet = [line.strip().split('\t') for line in flow_symbol.split('\n') if line]
        handler = tsv_handler.TSVHandler(packet)

    except Exception:
        print(traceback.format_exc())

    finally:
        directory = sys.modules[__name__]

        if hasattr(directory, 'handler'):
            print_f = pretty_print.PrettyPrint(handler)
            #print_f.pretty_print()
