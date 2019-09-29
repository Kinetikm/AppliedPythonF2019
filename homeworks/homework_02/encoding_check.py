import chardet


def encode_check(filename: str)->str:
    encodings = ['utf-8', 'utf-16', 'windows-1251']
    for encode in encodings:
        try:
            open(filename, encoding=encode).read()
            # with open(filename, encoding=encode):
            #     return encode
        # finally:
        #     return "fileValidationError"
        except (UnicodeDecodeError, LookupError, UnicodeError):
            pass
        else:
            return encode
    # with open(filename, 'r+b') as f:
    #     jsonf = b""
    #     for line in f:
    #         jsonf += line
    #     file_encoding = chardet.detect(jsonf)  # here we know encoding
    # if file_encoding['encoding'] in ['utf-8', 'windows-1251', 'utf-16']:
    #     return file_encoding['encoding']
    # else:
    #     return "fileValidationError"
