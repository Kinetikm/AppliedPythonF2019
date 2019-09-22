def reverse(number):
    number_2 = 0
    while number != 0:
        number_2 = number_2 * 10
        number_2 += number % 10
        number = number // 10
    return number_2
