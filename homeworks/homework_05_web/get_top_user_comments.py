import asyncio
import csv
import sys
from bs4 import BeautifulSoup
import aiohttp


async def fetch(session, url):
    try:
        async with session.get(url) as response:
            return await response.text()
    except aiohttp.ClientConnectionError:
        print('Connection err {}'.format(url))


async def fetch_all(urls):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        return await asyncio.gather(*[asyncio.ensure_future(fetch(session, url)) for url in urls])


def parser(html):
    comments = {}
    userblock = BeautifulSoup(html, 'html.parser').find_all('a', {"class": "user-info user-info_inline"})
    usernames = [username['data-user-login'] for username in userblock]
    for user in usernames:
        if user in comments:
            comments[user] += 1
        else:
            comments[user] = 1
    return comments


def writeCSV(data, filename):
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        writer.writerow(('link', 'username', 'count_comment'))
        for line in data:
            writer.writerow(line)


def main(filename, links):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(fetch_all(links))
    loop.run_until_complete(future)
    loop.close()
    data = []
    for i in range(len(future.result())):
        if future.result()[i] is not None:
            for key, val in parser(future.result()[i]).items():
                data.append((links[i], key, val))
    data.sort(key=lambda x: (x[0], -x[2]))
    writeCSV(data, filename)


if __name__ == '__main__':
    links = sys.argv[1:4]
    filename = 'top_user_comments.csv'
    main(filename, links)
