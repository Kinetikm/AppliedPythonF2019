import csv


def tsv_check(file, en):
    with open(file, 'r', encoding=en) as f:
        try:
            csv.reader(f)
            return True
        except:
            return False


def tsv_read(file, en):
    result = []
    with open(file, "r", encoding=en) as f:
        data = csv.reader(f, delimiter='\t')
        for i in data:
            result.append(i)
        return result
