
def print_table(table):
    dic = {}
    for i in range(len(table[0])):
        dlin = 0
        for k in range(len(table)):
            if len(table[k][i]) > dlin:
                dlin = len(table[k][i])
        dic[i] = dlin
    dlina_vsego = len(table[0]) * 5 + 1
    for k in dic:
        dlina_vsego += dic[k]
    for i in range(dlina_vsego-1):
        print("-", end='')
    print('-')
    for i in range(len(table[0])):
        print("|", end='')
        print(table[0][i].center(dic[i]+4), end='')
    print("|")
    for k in range(1, len(table)):
        for i in range(len(table[0])-1):
            print("|  ", end='')
            print(table[k][i], end='')
            for s in range(dic[i]-len(table[k][i])+2):
                print(" ", end='')
        print("|", end='')
        for s in range(dic[len(table[0])-1] - len(table[k][len(table[0])-1]) + 2):
            print(" ", end='')
        print(table[k][len(table[0])-1], end="")
        print("  |")
    for i in range(dlina_vsego):
        print("-", end='')
