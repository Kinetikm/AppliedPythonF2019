import sys
from bs4 import BeautifulSoup
import csv
import asyncio
import aiohttp

import sys
from bs4 import BeautifulSoup
import csv
import asyncio
import aiohttp


async def parser(link):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                r = await resp.text()
    except aiohttp.client_exceptions.ClientConnectorError:
        print("Connection error")
        return None
    soup = BeautifulSoup(r, "html.parser")
    dct = {}
    for t in soup.find_all('div', attrs={"class": ["comment"]}):
        usr = t.find('a')
        if usr is None:
            continue
        else:
            usr = usr.text.replace('\n', '')
        if dct.get(usr) is None and usr is not None:
            dct[usr] = 1
        elif usr is not None:
            dct[usr] += 1
    tmp_lst = []
    for x in map(lambda x: [link] + list(x), zip(dct.keys(), dct.values())):
        tmp_lst.append(x)
    return tmp_lst


async def body(filename, links):
    tasks = [asyncio.ensure_future(parser(link)) for link in links]
    list_users = await asyncio.gather(*tasks)
    asyncio.gather(*tasks)
    new_list = []
    if list_users is None:
        return
    for item in list_users:
        if item is not None:
            new_list += item
    list_users = new_list
    list_users = sorted(list_users, key=lambda lst: (lst[0], lst[2]),
                        reverse=True)

    with open(filename, "a") as file:
        print(list_users)
        csv_writer = csv.writer(file, delimiter=',')
        csv_writer.writerow(('link', 'username', 'count_comment'))
        [csv_writer.writerow(t) for t in list_users]
        file.close()


def main(filename, links):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(body(filename, links))
    loop.run_until_complete(future)


if __name__ == '__main__':
    filename = 'top_user_comments.csv'
    links = sys.argv[1:4]

    main(filename, links)
