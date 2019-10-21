import sys
from bs4 import BeautifulSoup
import csv
import asyncio
import aiohttp


async def parser(link):
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as resp:
            r = await
            resp.text()
    soup = BeautifulSoup(r, "html.parser")
    dct = {}
    for t in soup.find_all('div', attrs={"class": ["comment"]}):
        usr = t.find('a')
        if usr == None:
            continue
        else:
            usr = usr.text.replace('\n', '')
        if dct.get(usr) == None and usr != None:
            dct[usr] = 1
        elif usr != None:
            dct[usr] += 1
    tmp_lst = []
    for x in map(lambda x: [link] + list(x), zip(dct.keys(), dct.values())):
        tmp_lst.append(x)
    return tmp_lst


async def body(filename, links):
    tasks = [asyncio.ensure_future(parser(link)) for link in links]
    list_users = await
    asyncio.gather(*tasks)
    new_list = []
    for item in list_users:
        new_list += item
    list_users = new_list
    list_users = sorted(list_users, key=lambda lst: (lst[0], lst[2]),
                        reverse=True)
    
    with open(filename, "a") as file:
        print(list_users)
        csv_writer = csv.writer(file, delimiter=',')
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
