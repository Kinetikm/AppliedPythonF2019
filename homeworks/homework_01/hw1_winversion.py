def word_inversion2(input_lst):
    input_lst = ''.join(input_lst).split()[::-1]
    input_lst = ' '.join(input_lst)
    return list(input_lst)
