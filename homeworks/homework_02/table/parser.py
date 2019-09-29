
from io import StringIO
import json
import csv
from copy import copy

columns_order = ['Название', "Ссылка", "Теги", "Оценка"]


# возвращаем в формате более похожем на tsv
def parse_table(data: str):
    try:
        json_data = json.loads(data)
        res = [copy(columns_order)]
        for json_row in json_data:
            res.append([json_row[key] for key in columns_order])
        return res
    except ValueError:
        pass

    f = StringIO(data)
    return list(csv.reader(f, delimiter='\t'))
