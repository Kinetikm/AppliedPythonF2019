import json


def read_json(data):
    try:
        data = json.loads(data)
        return ["json", data]
    except:
        return None


def read_csv(data):
    try:
        data = data.split("\n")
        return ["csv", data]
    except:
        raise


def format_change(data):
    dt = read_json(data)
    if not dt:
        dt = read_csv(data)
    return dt
