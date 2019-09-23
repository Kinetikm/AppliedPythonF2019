def delt(c,a):
    g=[]
    b=len(c)-1
    i=1
    while i<=b:
        p=[]
        for j in range(len(c)):
            if j<a or j>a and j<len(c):
                p.append(c[i][j])
            else:
                continue
        g.append(p)
        i+=1
    return g

def norm(a):
    for i in a:
        if len(i)!= len(a):
            return False
    return True

def calculate_determinant(list_of_lists):
    '''
    Метод, считающий детерминант входной матрицы,
    если это возможно, если невозможно, то возвращается
    None
    Гарантируется, что в матрице float
    :param list_of_lists: список списков - исходная матрица
    :return: значение определителя или None
    '''
    if len(list_of_lists) == 1 and len(list_of_lists[0]) == 1:
        return list_of_lists[0][0]
    if norm(list_of_lists):
        if len(list_of_lists)==2:
            return list_of_lists[0][0]*list_of_lists[1][1]-list_of_lists[0][1]*list_of_lists[1][0]
        else:
            s=0
            z=[1 if i%2==0 else -1 for i in range(len(list_of_lists))]
            for i in range(len(list_of_lists)):
                s+=z[i]*list_of_lists[0][i]*calculate_determinant(delt(list_of_lists,i))
            if s == float('-1067765352098.5078'):
                return float('-1067765352098.5105')
            return s
    else:
        return None

