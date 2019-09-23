def reverse(number):
    if (number == 0):
        return 0
    d = str(number)
    d = d.rstrip('0')
    d = d[::-1]
    if '-' in d:
        d = d.rstrip('-')
        d = '-'+d
        return int(d)
    else:
        return int(d)
