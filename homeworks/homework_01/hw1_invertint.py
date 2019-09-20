def reverse(number):
    k = 0
    if number < 0:
        k = 1
        number = -number
    a = str(number)
    if k == 1:
        return int(a[::-1]) * (-1)
    else:
        return int(a[::-1])

