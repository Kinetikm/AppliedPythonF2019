def find_indices(input_list, target):
    if len(input_list) == 0:
        return None
    b = sorted(input_list[::])
    k = 0
    m = len(input_list) - 1
    while True:
        if k == m:
            return None
        elif b[k] + b[m] > target:
            m = m - 1
        elif b[k] + b[m] < target:
            k = k + 1
        else:
            break
    idx1 = input_list.index(b[k])
    idx2 = input_list.index(b[m])
    if idx1 < idx2:
        p = (input_list.index(b[k]), input_list.index(b[m]))
    else:
        p = (input_list.index(b[m]), input_list.index(b[k]))
    return p
