import json


def read_data(text):
    try:
        text = json.loads(text)
    except Exception:
        try:
            text = [i.split("\t") for i in text.strip().split("\n")]
            if len(text) > 2:
                text = [{text[0][k]: cell for k, cell in enumerate(
                    line)} for i, line in enumerate(text) if i > 0]
        except Exception:
            return None
    return text
