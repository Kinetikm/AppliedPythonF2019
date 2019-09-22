def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    if number == 0:
        return 0
    sign = 1      
    s = str(number)
    if s[0] == '-':
        sign = -1
        s = s[-1::]
    s = s[::-1]
    while (s[0] == "0"): 
        s=s[-1::]
    return int(s)*sign
    raise NotImplementedError
