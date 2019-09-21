def find_space(cur_pos, input_lst):
    i = cur_pos
    while (i != len(input_lst)) and (input_lst[i] != " "):
        i += 1
    return i


def word_inversion(input_lst):
    # reverse array
    for i in range(len(input_lst) // 2):
        input_lst[i], input_lst[-i - 1] = input_lst[-i - 1], input_lst[i]

    # reverse word
    next_space_pos = -1
    cur_space_pos = -1
    while next_space_pos < (len(input_lst)):
        cur_space_pos = next_space_pos
        next_space_pos = find_space(cur_space_pos + 1, input_lst)
        for i in range((next_space_pos - cur_space_pos) // 2):
            input_lst[cur_space_pos + i + 1], input_lst[next_space_pos - i - 1] = input_lst[next_space_pos - i - 1], \
                                                                                  input_lst[
                                                                                      cur_space_pos + i + 1]  # swap
    return input_lst
