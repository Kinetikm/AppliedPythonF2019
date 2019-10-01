# -*- coding: utf-8 -*-
import sys

# Ваши импорты
from json_file import json_data
from formater_text import text_formater, text_formater_tsv
from tsv_file import tsv_data

if __name__ == '__main__':
    filename = sys.argv[1]

    # Ваш код
    err = False
    err_not_fount = False
    data = {}
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
        print(unicode(text_formater(data), "utf-8"))
    else:
        try:
            data = tsv_data(filename, 'utf8')
            print(unicode(text_formater_tsv(data), "utf-8"))
        except FileNotFoundError:
            if not err_not_fount:
                print('Файл не валиден')
        except (UnicodeEncodeError, UnicodeDecodeError):
            try:
                data = tsv_data(filename, 'cp1251')
            except (IndexError, TypeError, KeyError, ValueError):
                print("Формат не валиден")
            print(unicode(text_formater_tsv(data), "utf-8"))
        except (IndexError, TypeError, KeyError):
            print("Формат не валиден")
