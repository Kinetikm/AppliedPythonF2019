import sys

import asyncio
import aiohttp
from bs4 import BeautifulSoup
import csv


async def get_stat(stat, link):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(link) as resp:
                local_stat = {}

                comments = BeautifulSoup(await resp.text(), "html.parser").find_all(
                    "a",
                    attrs={"class": "user-info user-info_inline"}
                )

                for comment in comments:
                    user_name = comment.attrs['data-user-login']
                    if user_name not in local_stat:
                        local_stat[user_name] = 1
                    else:
                        local_stat[user_name] += 1

                stat[link] = sorted(local_stat.items(), key=lambda x: x[1], reverse=True)
        except aiohttp.client_exceptions.ClientConnectorError:
            pass


def main(filename, links):
    statistic = {}
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.gather(
            *(get_stat(statistic, link) for link in links)
        )
    )

    with open(filename, mode='w') as file:
        file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(['link', 'username', 'count_comment'])
        for link, commentator in sorted(statistic.items(), key=lambda x: x[0], reverse=True):
            for username, count_comment in commentator:
                file_writer.writerow([link, username, count_comment])


if __name__ == '__main__':
    filename = 'top_user_comments.csv'
    links = sys.argv[1:4]
    main(filename, links)
