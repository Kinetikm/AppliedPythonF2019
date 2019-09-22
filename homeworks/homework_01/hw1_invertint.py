def reverse(number):
    if number == 0:
        return 0
    s = str(number)
    s = s.rstrip('0')
    s = s[::-1]
    if '-' in s:
        s = s.rstrip('-')
        s = '-'+s
        return(int(s))
    else:
        return(int(s))
