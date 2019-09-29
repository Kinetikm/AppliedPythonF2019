import csv


def define_tsv(file, enc):
    with open(file, 'r', encoding=enc) as f:
        try:
            csv.reader(f)
            return True
        except:
            return False


def tsv_tab(file, enc):
    with open(file, 'r', encoding=enc) as f:
        table = []
        data = csv.reader(f, delimiter='\t')
        for line in data:
            table.append(line)
        return table
