import sys
import enc
import json_read

if __name__ == '__main__':
    filename = sys.argv[1]

try:
    f = open(filename, "r")
    f.close()
except:
    print('Файл не валиден')
    sys.exit()
en = enc(filename)
if en not in ('utf-8', 'utf-16', 'cp1251'):
    print("...")
    sys.exit()
if json_check(filename, en):
    print(json_read(filename, en))
