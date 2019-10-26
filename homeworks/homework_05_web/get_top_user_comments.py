import sys
from collections import Counter
from bs4 import BeautifulSoup
from aiohttp import ClientSession
import asyncio
import csv


async def do_request(link, session):
    async with session.get(link) as resp:
        return link, await resp.read()


def main(filename, links):
    loop = asyncio.get_event_loop()
    responses = asyncio.ensure_future(run(links))
    loop.run_until_complete(responses)
    result = []
    if responses.result() is not None:
        for response in responses.result():
            resp_cnt = Counter()
            html = BeautifulSoup(response[1], 'html.parser')
            for tag in html.findAll('a'):
                if 'data-user-login' in tag.attrs:
                    resp_cnt[tag.attrs['data-user-login']] += 1

            resp_cnt = [[comm, resp_cnt[comm]] for comm in resp_cnt]
            resp_cnt.sort(key=lambda a: (a[1], a[0]), reverse=True)
            result.append({'link': response[0], 'stat': resp_cnt})
        result.sort(key=lambda a: a['link'])
    with open(filename, 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(["link", "username", "count_comment"])
        for link_result in result:
            for stat in link_result['stat']:
                writer.writerow([link_result['link'], stat[0], stat[1]])


async def run(links):
    try:
        requests = []
        async with ClientSession() as session:
            for link in links:
                req = asyncio.ensure_future(do_request(link, session))
                requests.append(req)
            return await asyncio.gather(*requests)
    except BaseException:
        return None

if __name__ == '__main__':
    filename = 'top_user_comments.csv'
    links = sys.argv[1:4]

    main(filename, links)
