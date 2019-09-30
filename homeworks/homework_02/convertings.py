import csv


from checkers import is_int


def print_tabs(s, len_of, out):
    c = 0
    if len(list(s.values())) != 0:
        while c < len(min(list(s.values()), key=len)):
            tab = "|"
            for key in s:
                k = len_of[key] - len(s[key][c]) - 3
                if check_int(s[key][c]):
                    tab = tab + " " * k + s[key][c] + "  " + "|"
                else:
                    tab = tab + "  " + s[key][c] + " " * k + "|"
            c += 1
            out.append(tab)


def json_to_table(data, out):
    s = {}
    len_of = {}
    for d in data:
        for key in d:
            if key in s:
                s[key].append(str(d[key]))
            else:
                s[key] = [str(d[key])]
            len_of[key] = max(s[key], key=len)
            len_of[key] = len(len_of[key])
            if len(str(key)) > len_of[key]:
                len_of[key] = len(str(key))
            len_of[key] += 5
    sum = 0
    for key in len_of:
        sum += len_of[key]
    out.append("-"*(sum+1))
    title = "|"
    for key in len_of:
        k = " "*((len_of[key]-len(key)-1)//2)
        title = title + k + key + k + '|'
    out.append(title)
    print_tabs(s, len_of, out)
    out.append("-"*(sum+1))


def tsv_to_table(file, e, out):
    len_of = []
    c = 0
    reader = open(file, encoding=e)
    data = csv.reader(open(file, encoding=e), delimiter="\t")
    for row in data:
        if c == 0:
            for r in row:
                len_of.append(len(str(r)))
            c = 1
        else:
            for i in range(len(row)):
                if len_of[i] < len(str(row[i])):
                    len_of[i] = len(str(row[i]))
    for i in range(len(len_of)):
        len_of[i] += 5
    s = 0
    for key in len_of:
        s += key
    out.append("-" * (s + 1))
    c = 0
    reader.close()
    data = csv.reader(open(file, encoding=e), delimiter="\t")
    for row in data:
        tab = "|"
        if c == 0:
            for i in range(len(row)):
                k = " "*((len_of[i]-len(row[i])-1)//2)
                tab = tab + k + row[i] + k + '|'
            c = 1
        else:
            for i in range(len(row)):
                k = len_of[i] - len(row[i]) - 3
                if check_int(row[i]):
                    tab = tab + " " * k + row[i] + "  " + "|"
                else:
                    tab = tab + "  " + row[i] + " " * k + "|"
        out.append(tab)
    out.append("-"*(s+1))
    reader.close()
