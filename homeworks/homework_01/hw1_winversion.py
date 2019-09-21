def find_comma(cur_pos, input_lst):
    i = cur_pos
    while (i != len(input_lst)) and (input_lst[i] != ("," or " ")):
        i += 1
    return i


def word_inversion(input_lst):
    # reverse array
    for i in range(len(input_lst) // 2):
        input_lst[i], input_lst[-i - 1] = input_lst[-i - 1], input_lst[i]

    # reverse words
    next_comma_pos = -1
    cur_comma_pos = -1
    while next_comma_pos < (len(input_lst)):
        cur_comma_pos = next_comma_pos
        next_comma_pos = find_comma(cur_comma_pos + 1, input_lst)
        for i in range((next_comma_pos - cur_comma_pos) // 2):
            input_lst[cur_comma_pos + i + 1], input_lst[next_comma_pos - i - 1] = input_lst[next_comma_pos - i - 1], \
                                                                                  input_lst[
                                                                                      cur_comma_pos + i + 1]  # swap
    return None
