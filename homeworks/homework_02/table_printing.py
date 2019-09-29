import sys


def table_print(mas: list):
    symbols_limit = []
    len_line = len(mas[0])
    checker = True
    for i in range(len(mas)):
        if len(mas[i]) != len_line:
            checker = False
    for i in range(len(mas[0])):
            symbols_limit.append(len(str(mas[0][i])))
    for i in range(len(mas)):
        for j in range(len_line):
            if len(str(mas[i][j])) > symbols_limit[j]:
                symbols_limit[j] = len(str(mas[i][j]))
    sum = 0
    for i in symbols_limit:
        sum += i
    if checker:
        sys.stdout()
        print(''.center(sum + 5*len_line + 1, '-'))

        print('| ', str(mas[0][0]).center(symbols_limit[0]), end=" ")
        for i in range(1, len(mas[0]) - 1):
            print(' | ', str(mas[0][i]).center(symbols_limit[i]), end=" ")
        print(' | ', str(mas[0][-1]).center(symbols_limit[-1]), ' |')

        for line in range(1, len(mas)):
            print('| ', str(mas[line][0]).ljust(symbols_limit[0]), end=" ")
            for i in range(1, len(mas[line]) - 1):
                print(' | ', str(mas[line][i]).ljust(symbols_limit[i]), end=" ")
            print(' | ', str(mas[line][-1]).rjust(symbols_limit[-1]), ' |')

        print(''.center(sum + 5*len_line + 1, '-'))
    else:
        print("Файл не валиден")
