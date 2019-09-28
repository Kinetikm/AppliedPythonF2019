def column_lenght(list_of_lists):
    max_wosrd_lenght = [0] * len(list_of_lists[0])
    for line in list_of_lists:
        for q in range(len(list_of_lists[0])):
            max_wosrd_lenght[q] = max(max_wosrd_lenght[q], len(str(line[q])))
    return max_wosrd_lenght
