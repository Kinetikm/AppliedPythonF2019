from read_file import *


if __name__ == '__main__':
    filename = sys.argv[1]
    list = read_file(filename)
    if list is not None:
        width = {}
        e = 0
        for i in list.keys():
            width[i] = len(str(list[i][0]))
            for elem in list[i]:
                e += 1
                if width[i] < len(str(elem)):
                    width[i] = len(str(elem))
            width[i] = (width[i] // 2) * 2
        s = len(width) * 11 + 1
        for i in width.keys():
            s += width[i]
        print('-' * s)
        for elem in list.keys():
            print("|" + elem.center(width[elem] + 10, " "), end="")
        print("|")
        e //= 4
        for i in range(e):
            for elem in list.keys():
                print("|" + 2 * " " + str(list[elem][i]) + " " * (width[elem] + 8 - len(str(list[elem][i]))), end="")
            print("|")
        print('-' * s)
