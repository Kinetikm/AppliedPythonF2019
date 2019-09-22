def reverse(number):
    if number == 0:
        return number
    s = str(number) if number > 0 else str((-1) * number)
    s = s[:: -1]
    while s[0] == '0':
        s = s[1:]
    return int(s) if number > 0 else (-1) * int(s)
