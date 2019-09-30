# -*- coding: utf-8 -*-
import sys
import traceback
# Ваши импорты
from json_file import json_data
from formater_text import text_formater
from tsv_file import tsv_data

if __name__ == '__main__':
    filename = sys.argv[1]
    data = {}
    # Ваш код
    err = False
    err_not_fount = False
    try:
        data = json_data(filename, 'utf8')
    except FileNotFoundError:
        err_not_fount = True
        print('Файл не валиден')
    except (UnicodeEncodeError, UnicodeDecodeError):
        try:
            data = json_data(filename, 'cp1251')
        except (FileNotFoundError, IndexError, TypeError, KeyError, ValueError):
            err = True
    except (IndexError, TypeError, KeyError, ValueError):
        err = True

    if not err and not err_not_fount:
        print(text_formater(data))
    else:
        try:
            data = tsv_data(filename, 'utf8')
            print(text_formater(data))
        except FileNotFoundError:
            if not err_not_fount:
                print('Файл не валиден')
        except (UnicodeEncodeError, UnicodeDecodeError):
            try:
                data = tsv_data(filename, 'cp1251')
            except (IndexError, TypeError, KeyError, ValueError):
                print("Формат не валиден")
            print(text_formater(data))
        except (IndexError, TypeError, KeyError):
            print("Формат не валиден")
