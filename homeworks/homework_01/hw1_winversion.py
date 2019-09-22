def word_inversion(input_lst):
    input_lst.reverse()
    index = 0
    for i in range(len(input_lst)):
        if (input_lst[i] == ' '):
            if (i - index != 1):
                input_lst[index:i] = input_lst[index:i][::-1]
                index = i + 1
            else:
                index = i + 1
    input_lst[index:] = input_lst[index:][::-1]
    return input_lst
