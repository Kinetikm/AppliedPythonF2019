import sys
from collections import Counter
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from bisect import insort
import asyncio

async def do_request(link, session):
    async with session.get(link) as resp:
        return await resp.read()

def main(filename, links):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(filename, links))
    loop.run_until_complete(future)

async def run(filename, links):
    requests = []
    result = []
    responses = []
    with open(filename, 'w') as file:
        file.write("{},{},{}\n".format("link","username","count_comment"))
    try:
        async with ClientSession() as session:
            for link in links:
                req = asyncio.ensure_future(do_request(link, session))
                requests.append(req)
            responses = await asyncio.gather(*requests)
    except:
        return
    for num_link, resp in enumerate(responses):
        resp_cnt = Counter()
        html = BeautifulSoup(resp, 'html.parser')
        for tag in html.findAll('a'):
            if 'data-user-login' in tag.attrs:
                resp_cnt[tag.attrs['data-user-login']] += 1

        result_resp = {}
        for key in resp_cnt:
            if resp_cnt[key] in result_resp:
                result_resp[resp_cnt[key]] += [key]
                continue
            result_resp[resp_cnt[key]] = [key]
        result.append({'link': links[num_link], 'result': result_resp})
    result.sort(key = lambda a: a['link'])

    with open(filename, 'a') as file:
        for link_result in result:
            counts_list = [key for key in link_result['result']]
            counts_list.sort()
            for cnt in counts_list:
                link_result['result'][cnt].sort()
                for username in link_result['result'][cnt]:
                    file.write("{},{},{}\n".format(link_result['link'],username,cnt)) 


if __name__ == '__main__':
    filename = 'top_user_comments.csv'
    links = sys.argv[1:4]

    main(filename, links)
