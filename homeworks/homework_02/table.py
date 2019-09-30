from argparse import ArgumentParser
from table_parser import JSONTableParser, TSVTableParser
from prettytable import PrettyTable


arg_parser = ArgumentParser()
arg_parser.add_argument('file_name', type=str)
arg_parser.add_argument('--encoding', type=str, default='utf-8')

args = arg_parser.parse_args()

text = ''
try:
    with open(args.file_name, 'r', encoding=args.encoding) as file:
        text = file.read()
except:
    exit('Файл не валиден')

table_parser_class = None
if text.lstrip().startswith('['):
    table_parser_class = JSONTableParser
else:
    table_parser_class = TSVTableParser

table_parser = table_parser_class(text)

try:
    columns, rows = table_parser.parse()
except:
    exit('Формат не валиден')

table = PrettyTable(columns)
for row in rows:
    table.add_row(row)

print(table)
