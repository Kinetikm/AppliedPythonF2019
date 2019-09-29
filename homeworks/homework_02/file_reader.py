import json
import os.path


def read_file(filename):
    if not os.path.exists(filename):
        return 1, None
    try:
        file = open(filename, encoding='utf-8')
        data = file.read()
    except (FileNotFoundError, FileExistsError) as err:
        return 1, None
    except UnicodeError:
        print('utf8 failed')
        file.close()
        try:
            file = open(filename, encoding='utf-16')
            data = file.read()
        except UnicodeError:
            print('utf16 failed')
            file.close()
            try:
                file = open(filename, encoding='cp1251')
                data = file.read()
            except ValueError:
                print('cp1251 failed')
                file.close()
                return 2, None
    finally:
        file.close()
    return 0, data
