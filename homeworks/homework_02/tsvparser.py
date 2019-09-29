import csv


def tsvparse(file):
    reader = csv.reader(file, delimiter='\t')
    rows = list(reader)
    linkslen = 0
    tagslen = 0
    namelen = 0
    for row in rows:
        if len(row[0]) > namelen:
            namelen = len(row[0])
        if len(row[1]) > linkslen:
            linkslen = len(row[1])
        if len(row[2]) > tagslen:
            tagslen = len(row[2])
    print('|  {tag:^{len}}'.format(tag='Название', len=namelen) +
          '  |  {tag:^{len}}'.format(tag='Ссылка', len=linkslen) +
          '  |  {tag:^{len}}'.format(tag='Теги', len=tagslen) + '  |  {tag:^{len}}'.format(tag='Оценка', len=1) + '  |')
    for row in rows[1:]:
        print('|  {tag:<{len}}'.format(tag=row[0], len=namelen) +
              '  |  {tag:<{len}}'.format(tag=row[1], len=linkslen) +
              '  |  {tag:<{len}}'.format(tag=row[2], len=tagslen) +
              '  |  {tag:>{len}}'.format(tag=row[3], len=6) + '  |')
