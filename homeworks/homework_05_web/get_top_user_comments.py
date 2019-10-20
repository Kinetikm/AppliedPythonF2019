import sys
import requests
from bs4 import BeautifulSoup
import csv
import aiohttp
import asyncio

# Ваши импорты

async def get_data(link):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                result = await resp.text()
                return link, result
    except aiohttp.client_exceptions.ClientConnectorError:
        print("Cannot open link {link}".format(link=link))


def parse_html(text):
    html = BeautifulSoup(text, 'html.parser')
    return Counter((
        span.getText()
        for span in html.findAll('span', attrs={'class': 'user-info__nickname_comment'})
    )).most_common()


def write_csv(data, filename):
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)


def main(urls, filename):
    lines = [['link', 'username', 'count_comment']]
    loop = asyncio.get_event_loop()
    pages = loop.run_until_complete(asyncio.gather(*(get_data(link) for link in urls)))
    loop.close()
    p = [i for i in p if i is not None]
    for link in urls:
        for text in p:
            for username, count_comment in parse_html(text):
                lines.append([link, username, count_comment])
    write_csv(lines, filename)



if __name__ == '__main__':
    filename = 'top_user_comments.csv'
    links = sys.argv[1:4]
    main(links, filename)
