def json_transfer(data):
    '''Функция, переводящая данные, которые мы считали с джисона
       в удобоваримый вид, плюс проверка на валидность данных.
       Итоговый формат: словарь, где по ключам раскиданы значения'''

    final = dict()
    for i in data:
        # проверка на валидность данных
        if type(i) != dict:
            return False
        a = i.items()
        a = list(a)
        for j in a:
            if len(j) == 0:
                return False
            if j[0] not in final:
                final[j[0]] = []
            final[j[0]].append(str(j[1]))
    return final


def tsv_transfer(data):
    '''Функция, переводящая данные, которые мы считали с тисиви
       в удобоваримый вид, плюс проверка на валидность данных
       Итоговый формат: словарь, где по ключам раскиданы значения'''
    temp = []
    final = dict()
    for mas in data:
        # длинную строку с табуляциями разбиваем и проверяем на пустоту
        if len(mas) == 0:
            return False
        temp.append(mas[0].split('\t'))
    # проверка на пустоту после разбивания
    if len(temp) == 0:
        return False
    for key in temp[0]:
        if key not in final:
            final[key] = []
    for inf in temp[1::]:
        # количество ключей должно совпадать с количеством объектов
        if len(inf) != len(temp[0]):
            return False
        for i in range(len(inf)):
            final[temp[0][i]].append(inf[i])
    return final
