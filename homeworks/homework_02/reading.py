import csv
import json
from table_printing import table_print


def reading_data(filename: str, encoding: str)->list:
    with open(filename, 'r', encoding=encoding) as f:
        mas = []
        jsonF = ""
        for line in f:
            jsonF += line
        try:
            json.loads(jsonF)
        except (TypeError, UnicodeError, SyntaxError, AttributeError, IndexError):
            pass
            # print("Формат не валиден")
        except FileNotFoundError:
            print('Файл не валиден')
        except json.decoder.JSONDecodeError:
            with open(filename, 'r', encoding=encoding) as ff:
                read = csv.reader(ff, delimiter="\t")
                for line in read:
                    mas.append(line)
            table_print(mas)

        else:
            jsonF = json.loads(jsonF)
            keys = list(jsonF[0].keys())
            mas.append(keys)
            for obj in jsonF:
                prom_mas = []
                for i in range(len(keys)):
                    prom_mas.append(obj[keys[i]])
                mas.append(prom_mas)
            table_print(mas)
