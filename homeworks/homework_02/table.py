import sys
from read_file import read_file
from decode import read_json
from decode import read_csv
from draw_table import draw_table 


if __name__ == '__main__':
    filename = sys.argv[1]        # comment

text = read_file(filename)
if text is None:
    print("Not valid format")
else:
    text_dict = read_json(text)
    if text_dict is None:
        text_dict = read_csv(text)
print(draw_table(text_dict))
return draw_table(text_dict)
