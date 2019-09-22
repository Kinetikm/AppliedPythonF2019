def check_palindrom(input_string):
    l = len(input_string)


    for i in range(l // 2):
        if input_string[i] != input_string[-1 - i]:
            #print("It's not palindrome")
            return False

    #print("It's palindrome")
    '''
    Метод проверяющий строку на то, является ли
    она палиндромом.
    :param input_string: строка
    :return: True, если строка являестя палиндромом
    False иначе
    '''
    return True
    raise NotImplementedError
