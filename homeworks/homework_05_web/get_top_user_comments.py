import sys
import requests
from bs4 import BeautifulSoup
import csv
import aiohttp
import asyncio


async def get_html(link):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                result = await resp.text()
                return link, result
    except aiohttp.client_exceptions.ClientConnectorError:
        print("Cannot open link {link}".format(link=link))


def pars(data):
    soup = BeautifulSoup(data, 'lxml')
    comments = soup.find_all('div', class_="comment")
    users_comments = {}
    for comment in comments:
        user_info = comment.find('a', class_="user-info user-info_inline")
        if user_info is not None:
            user_login = user_info['data-user-login']
            if user_login in users_comments:
                users_comments[user_login] += 1
            else:
                users_comments[user_login] = 1
    return users_comments


def process_page(page, link):
    data = pars(page)
    return [(link, key, value) for key, value in data.items()]


def write_csv(file_name, rows):
    rows.sort(key=lambda x: x[2], reverse=True)
    rows.sort(key=lambda x: x[0])
    with open(file_name, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(('link', 'username', 'count_comment'))
        for row in rows:
            writer.writerow(row)


def main(file_name, links):
    loop = asyncio.get_event_loop()
    pages = loop.run_until_complete(asyncio.gather(*(get_html(link) for link in links)))
    loop.close()
    pages = [i for i in pages if i is not None]
    data = []
    for link, page in pages:
        data += process_page(page, link)
    write_csv(file_name, data)


if __name__ == '__main__':
    filename = 'top_user_comments.csv'
    links = sys.argv[1:4]
    main(filename, links)
