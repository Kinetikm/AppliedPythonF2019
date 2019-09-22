import copy


def minor(list_of_lists, i, j):
    new_list = copy.deepcopy(list_of_lists)
    for k in range(len(list_of_lists)):
        del new_list[k][j]
    del new_list[i]
    return new_list


def calculate_determinant(list_of_lists):
    for i in range(len(list_of_lists)):
        if len(list_of_lists) != len(list_of_lists[i]):
            return None
    if len(list_of_lists) == 1:
        return list_of_lists[0][0]
    det = 0
    for j in range(len(list_of_lists)):
        det += ((-1)**j * list_of_lists[0][j] *
                calculate_determinant(minor(list_of_lists, 0, j)))
    return det
