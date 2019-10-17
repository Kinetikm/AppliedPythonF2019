import os
import sys
import aiohttp
import asyncio
from multiprocessing import Manager, Pool
from bs4 import BeautifulSoup
import csv

connector = aiohttp.TCPConnector(verify_ssl=False)


async def fetch(session, url):
    try:
        async with session.get(url) as response:
            return (await response.text(), url)
    except aiohttp.client_exceptions.ClientConnectorError:
        pass
        # но можно и грязно поругаться

async def fetch_all(urls):
    tasks = []
    async with aiohttp.ClientSession(connector=connector) as session:
        for url in urls:
            task = asyncio.ensure_future(fetch(session, url))
            tasks.append(task)
        return await asyncio.gather(*tasks)


def parse(params):
    soup = BeautifulSoup(params['text'], 'lxml')
    comments_heads = soup.findAll('div', class_="comment__head")
    users_comments = {}
    for comment in comments_heads:
        user_info = comment.find('a', class_="user-info user-info_inline")
        user_login = user_info['data-user-login']
        if user_login in users_comments:
            users_comments[user_login] += 1
        else:
            users_comments[user_login] = 1
    params['res'][params['url']] = users_comments


def write_csv(rows, filename):
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(('link', 'username', 'count_comment'))
        for row in rows:
            writer.writerow(row)


def struct_result(res):
    structed_res = []
    for url in res.keys():
        for user_login, cnt in res[url].items():
            structed_res.append((url, user_login, cnt))
    structed_res.sort(key=lambda x: x[2], reverse=1)
    structed_res.sort(key=lambda x: x[0])
    return structed_res


def main(filename, urls):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(fetch_all(urls))
    loop.run_until_complete(future)
    res = Manager().dict()
    if (not (future.result()[0] is None)):
        optimal = len(future.result()) if (os.cpu_count() > len(future.result())) else os.cpu_count()
        pool = Pool(optimal)
        args_for_map = map(lambda x: {'text': x[0], 'url': x[1], 'res': res}, future.result())
        pool.map(parse, args_for_map)
    write_csv(struct_result(res), filename)

if __name__ == '__main__':
    urls = sys.argv[1:4]
    filename = 'top_user_comments.csv'
    main(filename, urls)
