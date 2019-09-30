def pretty_print_table(data):
    if data[0] == "json":
        text = data[1]
    if data[0] == "csv":
        text = data[1][:-1]

    if text is not None:
        row = {}
        e = 0
        for i in text.keys():
            row[i] = len(str(text[i][0]))
            for elem in text[i]:
                e += 1
                if row[i] < len(str(elem)):
                    row[i] = len(str(elem))
            row[i] = (row[i] // 2) * 2
        s = len(row) * 11 + 1
        for i in row.keys():
            s += row[i]
        print('-' * s)
        for elem in text.keys():
            print("|" + elem.center(row[elem] + 10, " "))
        print("|")
        e //= 4
        for i in range(e):
            for elem in text.keys():
                print("|" + 2 * " " + str(text[elem][i]) + " " * (row[elem] + 8 - len(str(text[elem][i]))))
            print("|")
        print('-' * s)