def check_palindrom(input_string):
    reversed_string = input_string[::-1]
    if (reversed_string == input_string):
        return True
    else:
        return False
