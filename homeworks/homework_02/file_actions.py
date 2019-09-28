import json
import csv

from chardet.universaldetector import UniversalDetector

from validation import check_json
from formatting import tsv_to_json


def get_encoding_file(path: str) -> str:
    detector = UniversalDetector()
    with open(path, "rb") as fh:
        for line in fh:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    return detector.result["encoding"]


def get_data_from_file(file_path):
    enc = get_encoding_file(file_path)

    with open(file_path, encoding=enc) as read_file:

        if check_json(file_path, enc):
            data = json.load(read_file)
        else:
            data = []
            tsv_data = csv.reader(read_file, delimiter="\t")
            for row in tsv_data:
                data.append(row)

            data = tsv_to_json(data)

    return data
