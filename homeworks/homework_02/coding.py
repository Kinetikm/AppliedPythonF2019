import chardet


def detect_coding(string):
    encoding = chardet.detect(string)
    return encoding['encoding']
