import sys
from bs4 import BeautifulSoup
from csv import writer
from aiohttp import ClientSession, client_exceptions
from asyncio import gather, ensure_future, get_event_loop

async def get_url(urls, url, session):
    try:
        async with session.get(url[1]) as resp:
            return await resp.text()
    except client_exceptions.ClientConnectorError:
        urls.remove(url)


async def fetch_all(urls):
    async with ClientSession() as session:
        results = await gather(*[ensure_future(get_url(urls, url, session)) for url in urls])
    return results


def main(filename, links):
    with open(filename, 'w') as f:
        write = writer(f, lineterminator='\n')
        write.writerows([['link', 'username', 'count_comment']])
    loop = get_event_loop()
    urls = [[i, links[i]] for i in range(len(links))]
    files = loop.run_until_complete(fetch_all(urls))
    urls.sort(key=lambda x: x[1], reverse=True)
    for fil in urls:
        comments = dict()
        soup_object = BeautifulSoup(files[fil[0]], 'html.parser')
        usernames = soup_object.find_all('span', {'class': 'user-info__nickname \
user-info__nickname_small user-info__nickname_comment'})
        for i in usernames:
            if i.next in comments:
                comments[i.next] += 1
            else:
                comments[i.next] = 1
        csv_data = [[fil[1], i, comments[i]] for i in comments]
        csv_data = sorted(csv_data, key=lambda x: x[2], reverse=True)
        with open(filename, 'a') as f:
            write = writer(f, lineterminator='\n')
            write.writerows(csv_data)


if __name__ == '__main__':
    filename = 'top_user_comments.csv'
    links = sys.argv[1:4]

    main(filename, links)
