def calculate_determinant(list_of_lists):
    '''
    Метод, считающий детерминант входной матрицы,
    если это возможно, если невозможно, то возвращается
    None
    Гарантируется, что в матрице float
    :param list_of_lists: список списков - исходная матрица
    :return: значение определителя или None
    '''
    det = 0
    if len(list_of_lists) != len(list_of_lists[0]):
        return None
    if len(list_of_lists) == 2:
        return (list_of_lists[0][0] * list_of_lists[1][1] - list_of_lists[0][1] * list_of_lists[1][0])
    for i in range (len(list_of_lists[0])):
        a = []
        for j in range (1,len(list_of_lists)):
            a.append(list_of_lists[j][0:i] + list_of_lists[j][i+1:])
        det += (-1) ** i * list_of_lists[0][i] * calculate_determinant(a)
    return(det)
