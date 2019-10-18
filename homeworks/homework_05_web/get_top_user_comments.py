import sys
import csv
from bs4 import BeautifulSoup
import aiohttp
import asyncio


async def request(session, link):
    try:
        async with session.get(link) as response:
            return link, await response.text()
    except aiohttp.ClientConnectionError:
        print(f'Conn error {link}')


async def fetch_all(links):
    tasks = []
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:  # Коннектор чтобы
        # отключить проверку SSL-сертификата, т.к. https запросы
        for link in links:
            tasks.append(asyncio.ensure_future(request(session, link)))
        return await asyncio.gather(*tasks)


def parse(text):
    users_comms = {}
    soup = BeautifulSoup(text, 'html.parser')
    comm_num = int(soup.find('span', class_='comments-section__head-counter').text)
    if comm_num < 100:
        return None
    comms = soup.findAll('div', class_='comment__head')
    for comm in comms:
        user = (comm.find('a', class_='user-info user-info_inline').get('data-user-login'))
        if user not in users_comms:
            users_comms[user] = 1
        else:
            users_comms[user] += 1
    return users_comms


def write_csv(filename, rows):
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['link', 'username', 'count_comment'])
        writer.writerows(sort_rows(rows))


def make_rows(link, html):
    rows = []
    users_comms = parse(html)
    for key, value in users_comms.items():
        rows.append((link, key, value))
    return rows


def sort_rows(rows):
    rows.sort(key=lambda x: (x[0], -x[2]))
    return rows


def main(filename, links):
    loop = asyncio.get_event_loop()
    pages = asyncio.ensure_future(fetch_all(links))
    loop.run_until_complete(pages)
    loop.close()
    all_rows = []
    for inx in range(len(pages.result())):
        if pages.result()[inx] is not None:
            link = pages.result()[inx][0]
            html = pages.result()[inx][1]
            if html:
                all_rows.extend(make_rows(link, html))
    write_csv(filename, all_rows)


if __name__ == '__main__':
    filename = 'top_user_comments.csv'
    links = sys.argv[1:4]

    main(filename, links)
