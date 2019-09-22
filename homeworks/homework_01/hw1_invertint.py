def reverse(number):
    if number < 0:
        sign = - 1
    else:
        sign = 1
    list_number = list(str(abs(number)))
    list_number.reverse()
    str_number = "".join(list_number)
    invert_number = int(str_number)
    return sign*invert_number
