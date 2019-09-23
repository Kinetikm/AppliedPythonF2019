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


def determinant(mat):
    if norm(mat):
        if (len(mat) == 2):
            return mat[0][0]*mat[1][1]-mat[0][1]*mat[1][0]
        else:
            sum = 0
            for i in range(len(mat)):
                sum += (-1)**(i)*mat[0][i]*determinant(delete(mat, i))
            return sum
    else:
        return None
