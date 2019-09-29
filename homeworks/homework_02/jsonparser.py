import json


def jsonparse(file):
    data = json.load(file)
    linkslen = 0
    tagslen = 0
    namelen = 0
    for item in data:
        if len(item['Ссылка']) > linkslen:
            linkslen = len(item['Ссылка'])
        if len(item['Теги']) > tagslen:
            tagslen = len(item['Теги'])
        if len(item['Название']) > namelen:
            namelen = len(item['Название'])
    print('|  {tag:^{len}}'.format(tag='Название', len=namelen)+'  |  {tag:^{len}}'.format(tag='Ссылка', len=linkslen) +
          '  |  {tag:^{len}}'.format(tag='Теги', len=tagslen)+'  |  {tag:^{len}}'.format(tag='Оценка', len=6)+'  |')
    for item in data:
        print('|  {tag:<{len}}'.format(tag=item['Название'], len=namelen) +
              '  |  {tag:<{len}}'.format(tag=item['Ссылка'], len=linkslen) +
              '  |  {tag:<{len}}'.format(tag=item['Теги'], len=tagslen) +
              '  |  {tag:>{len}}'.format(tag=item['Оценка'], len=6) + '  |')
