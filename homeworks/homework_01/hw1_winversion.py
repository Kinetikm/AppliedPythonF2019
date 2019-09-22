def word_inversion(input_lst):
    w = ''
    for i in range(len(input_lst)):
        char = input_lst.pop(0)
        if char == ' ':
            input_lst.append(w)
            w = ''
            continue
        w += char
    input_lst.append(w)
    input_lst.reverse()
    for i in range(len(input_lst)):
        if i == len(input_lst)-1:
            w = input_lst.pop(0)
            input_lst.append(w)
        else:
            w = input_lst.pop(0)
            input_lst.append(w+' ')
    w = ''
    for i in range(len(input_lst)):
        c = input_lst.pop(0)
        w += c
    input_lst.append(w)
    return list(input_lst[0])
