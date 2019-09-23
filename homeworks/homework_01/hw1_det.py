def delete(c, a):
    g = []
    i = 1
    while(i < len(c)):
        p = []
        for j in range(len(c)):
            if (j < a or j > a and j < len(c)):
                p.append(c[i][j])
            else:
                continue
        g.append(p)
        i += 1
    return g


def norm(a):
    for i in a:
        if len(i) != len(a):
            return False
    return True


def calculate_determinant(list_of_lists):
    width = len(list_of_lists)
    if norm(list_of_lists):
        if (len(list_of_lists) == 2):
            return list_of_lists[0][0] * list_of_lists[1][1] - list_of_lists[0][1] * list_of_lists[1][0]
        elif (len(list_of_lists) == 1):
            return list_of_lists[0][0]
        else:
            sum = 0
            for i in range(len(list_of_lists)):
                sum += (-1)**(i) * list_of_lists[0][i] * calculate_determinant(delete(list_of_lists, i))
            return sum
    else:
        return None
