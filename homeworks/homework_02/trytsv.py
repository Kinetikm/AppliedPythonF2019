import csv


def from_tsv(file, code):
    with open(file, encoding=code) as tsvfile:
        try:
            data = []
            header = None
            tsvreader = csv.reader(tsvfile, delimiter="\t")
            for i, a in enumerate(tsvreader):
                if i:
                    b = []
                    for num in a:
                        try:
                            b.append(int(num))
                        except:
                            b.append(num)
                    data.append({header[i]: b[i] for i in range(len(b))})
                else:
                    header = a
            return data
        except:
            return
