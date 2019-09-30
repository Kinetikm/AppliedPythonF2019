def parcer(l):
    z = []
    s = []
    dl = []
    if l[0] == "[":
        el = l.index("},") - 2
        dl = [0 for i in range(0, el, 1)]
        i = 0
        for j in range(0, el, 1):
            h = l[j + 2][1:l[j + 2].find(" ") - 2]
            z.append(h)
        while True:
            if l[1 + i * (el + 2)] == "]":
                break
            st = []
            for j in range(0, el - 1, 1):
                st.append(l[1 + i * (el + 2) + 1 + j])
                if st[j][1: st[j].find(" ") - 2] != z[j]:
                    return
                st[j] = st[j][st[j].find(" ") + 2: len(st[j]) - 2]
                if len(st[j]) > dl[j]:
                    dl[j] = len(st[j])
            st.append(l[1 + i * (el + 2) + 1 + (el - 1)])
            st[el - 1] = st[el - 1][st[el - 1].find(" ") + 1: len(st[el - 1])]
            if len(st[(el - 1)]) > dl[(el - 1)]:
                dl[(el - 1)] = len(st[(el - 1)])
            s.append(st[:])
            i = i + 1
        s.insert(0, z)
        for ii in range(0, len(z), 1):
            if len(z[ii]) > dl[ii]:
                dl[ii] = len(z[ii])
        s.append(dl)
    else:
        p = l[0].split("\t")
        n = len(p)
        dl = [0 for i in range(0, len(p), 1)]
        for i in l:
            p = i.split("\t")
            if len(p) != n:
                return
            s.append(p)
            for j in range(0, len(p), 1):
                if len(p[j]) > dl[j]:
                    dl[j] = len(p[j])
        s.append(dl)
    return s
