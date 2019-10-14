def print_text(text: list):
    """ Нужно узнать максимальный размер таблички в ширину. Для этого нужно узнать максимальный размер элемента в кождом
    столбце [[title, title],
             [value1, value2]
            ]
    Для максимально простой и удобной обработки таблицы хотел использовать модуль PrettyTable, но судя по описанию
    задачи, вывод нужно сделать самостоятельно и методы использовать только для центрирования. Для него выбрал
    shutil.
    """

    dict_len = {}

    for lists in text:
        for num, element in enumerate(lists):
            if num in dict_len:
                dict_len[num] = max(dict_len[num], len(str(element)))
            else:
                dict_len[num] = len(element)

    # Печать верхней полосочки
    max_len = 0
    for key_ellem in dict_len.keys():
        max_len += dict_len[key_ellem]

    print("-" * (max_len + 5 * len(text[0]) + 1))

    # Печать списка
    for lists in text:
        line = "|"
        for num, elems in enumerate(lists):
            if lists == text[0]:
                line = line + "  " + str(elems).center(dict_len[num]) + "  |"
            else:
                if num == len(lists) - 1:
                    line = line + "  " + str(elems).rjust(dict_len[num]) + "  |"
                else:
                    line = line + "  " + str(elems).ljust(dict_len[num]) + "  |"
        print(line)

    # Печать нижней полосочки
    print("-" * (max_len + 5 * len(text[0]) + 1))
