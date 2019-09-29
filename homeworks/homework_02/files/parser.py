import json
import sys
import os

filename = sys.argv[1]

encoding = os.path.splitext(filename)[0].split('-')[-1]
print(encoding)

with open(filename, encoding = encoding) as f:
    sturct = json.load(f)

print(sturct)
print(type(sturct))
print(type(sturct[0]))
