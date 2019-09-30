def writer(s):
    dl = s[len(s) - 1]
    sch = 0
    for i in dl:
        sch = sch + i
    sch = sch + (len(dl) * 5) + 1
    print('-' * sch)
    h = []
    for i in range(0, len(dl), 1):
        h.append(s[0][i])
        h[i] = h[i].center(dl[i] + 4)
    st = ""
    for i in h:
        st = st + i + "|"
    print('|' + st)
    s.pop(0)
    s.pop()
    for i in s:
        st = ""
        for j in range(0, len(i) - 1, 1):
            st = st + "  " + i[j]
            pr = ' ' * (dl[j] - len(i[j]) + 2)
            st = st + pr + "|"
        j = len(i) - 1
        pr = ' ' * (dl[j] - len(i[j]) + 2)
        st = st + pr + i[j] + "  " + "|"
        print('|' + st)
    print('-' * sch)
