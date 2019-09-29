import sys
import coding
import readtsv
import drawtab
import filetype


if __name__ == '__main__':
    filename = sys.argv[1]
    try:
        with open(filename, "rb") as file:
            string = file.read()
    except FileNotFoundError:
        print("Файл не валиден")
    else:
        coding = coding.detect_coding(string)
        result = filetype.define_type(filename, coding)
        if type(result) == str:
            data = readtsv.read(filename, coding)
        else:
            data = result
        if data:
            drawtab.draw_table(data)
