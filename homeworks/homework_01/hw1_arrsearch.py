def find_indices(input_list, target):
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
    p = (a.index(b[k]), a.index(b[m]))
    return p



