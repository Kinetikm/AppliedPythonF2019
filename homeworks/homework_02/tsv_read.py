import csv


def is_tsv(file, enc):
    with open(file, 'r', encoding=enc) as f:
        try:
            csv.reader(f)
            return True
        except:
            return False


def tsv_read(file, enc):
    with open(file, 'r', encoding=enc) as f:
        table_data = []
        data = csv.reader(f, delimiter='\t')
        for row in data:
            table_data.append(row)
        return table_data
