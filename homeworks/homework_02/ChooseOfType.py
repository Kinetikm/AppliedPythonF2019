import json
import csv


def option_csv(input_data):
    try:
        input_data = csv.reader(input_data, delimiter="\t")
        return ["csv_file", input_data]
    except:
        return None


def option_json(input_data):
    try:
        input_data = json.loads(input_data)
        jsoner = input_data
        keys = jsoner[0].keys()
        input_data = ["\t".join(keys)]

        for record in jsoner:
            line = []
            for key in keys:
                line.append(str(record[key]))

            input_data.append("\t".join(line))
        return ["json_file", input_data]
    except:
        return None


def choose_type(input_data):
    data = option_csv(input_data)
    if data:
        return data
    data = option_json(input_data)
    if data:
        return data
    if not data:
        raise FileNotFoundError
