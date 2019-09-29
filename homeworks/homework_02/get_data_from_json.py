import json


def get_data_from_json(filename, encoding):
    with open(filename, 'r', encoding=encoding) as json_file:
        try:
            data = json.load(json_file)
            list_of_data = [[]]
            for key in data[0]:
                list_of_data[0].append(key)
            for i in range(len(data)):
                list_of_data.append([])
                for j in list_of_data[0]:
                    list_of_data[i+1].append(' ' + str(data[i][j]) + ' ')
            return list_of_data
        except OSError:
            print("Файл не валиден")
            raise SystemExit







