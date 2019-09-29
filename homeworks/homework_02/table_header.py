def table_header(name_of_row=[], max_of_lens=[]):
    str_ = '|'
    i = 0
    for _ in name_of_row:
        if len(_) < max_of_lens[i]:
            str_ += 2*' ' + _.center(max_of_lens[i]) + '  |'
        else:
            str_ += 2*' ' + _ + '  |'
        i += 1
    str_ = '-' * len(str_) + '\n' + str_
    return str_
