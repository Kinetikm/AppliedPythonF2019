def word_inversion(input_lst):
    k = 0
    for i in range(len(input_lst)):
        if input_lst[i] == " ":
            input_lst[k:i:] = input_lst[k:i:][::-1]
            k = i + 1
    input_lst[k::] = input_lst[k::][::-1]
    input_lst = input_lst[::-1]
    return input_lst


'''
a = ['О', ' ', 'П', 'р', 'и', 'в', 'е', 'т', ' ', 'О', ' ', 'к', 'а', 'к', ' ', 'д', 'е', 'л', 'а']
print(word_inversion(a))
'''
