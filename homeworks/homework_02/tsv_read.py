import csv


def tsv_check(file, en):
    with open(file, 'r', encoding=en) as f:
        try:
            data = csv.reader(f, delimiter="\t")
            m = 0
            for i in data:
                if m != len(i) and m != 0:
                    return False
                m = len(i)
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
