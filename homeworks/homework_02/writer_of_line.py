def writer_of_line(list_of_line, list_of_maxint, name_of_row):
    forma = '  %s%s  |'
    str_ = '|'
    j = 0
    for i in list_of_line:
        space_ = max(list_of_maxint[j], len(name_of_row[j]))
        if i == list_of_line[-1]:
            str_ += forma % ((space_ - len(i)) * ' ', i)
        else:
            str_ += forma % (i, (space_ - len(i)) * ' ')
        j += 1
    return str_
