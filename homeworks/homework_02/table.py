import sys
import reader as a
import writer as c
import parсer as b

if __name__ == '__main__':
    filename = sys.argv[1]
    ind = True
    try:
        l = a.reader(filename)
    except FileNotFoundError:
        print("Файл не валиден")
        ind = False
    if l is None and ind:
        print("Формат не валиден")
    else:
        if ind:
            ll = b.parcer(l)
    if ll is None and ind:
        print("Формат не валиден")
    else:
        if ind:
            c.writer(ll)
