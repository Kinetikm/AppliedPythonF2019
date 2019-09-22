def reverse(number):
    d = number
    d = str(d)
    d = d[::-1]
    if '-' in d:
        d = d.rstrip('-')
        d = '-'+d
        return(int(d))
    else:
        return(int(d))

