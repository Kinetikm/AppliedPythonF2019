def check_type_codding(file_path):
    for i in ('utf8', 'utf16', 'cp1251'):
        try:
            with open(file=file_path, mode="r", encoding=i) as fp:
                line = fp.readline()
                return i
        except UnicodeError:
            pass
        except FileNotFoundError:
            return 'Файл не валиден'
        except Exception:
            return 'Формат не валиден'
