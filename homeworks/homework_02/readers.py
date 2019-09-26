import json
import csv


def read_json(file):
    """
    read data from json file
    :param file: file descriptor
    :return: - list of columns row, firs row is header, each row is list of entries
             - None if file not valid json
    """
    try:
        data = json.load(file)
        columns = list(data[0].keys())
        result = [columns]
        for item in data:
            result.append([item[key] for key in columns])
        return result
    except json.JSONDecodeError:
        return None


def read_tsv(file):
    """
    read data from tsv file
    :param file: file descriptor
    :return: - list of columns row, firs row is header, each row is list of entries
             - None if file not valid json
    """
    try:
        dialect = csv.Sniffer().sniff(file.read(1024), delimiters="\t")
        reader = csv.reader(file, dialect=dialect)
        data = [line for line in reader]
        return data
    except csv.Error:
        return None
