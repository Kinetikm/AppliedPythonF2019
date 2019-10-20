import sys
import csv
import asyncio
import aiohttp
from collections import Counter
from bs4 import BeautifulSoup


async def get_text(link):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                result = await resp.text()
                return [result, link]
    except aiohttp.client_exceptions.ClientConnectorError:
        return


def write_to_file(filename, link, count_comment):
    with open(filename, "a") as fs:
        writer = csv.writer(fs)
        for key, value in sorted(count_comment.items(), key=lambda x: (x[1], x[0]), reverse=True):
            writer.writerow([link, key, value])


def main(filename, links):
    with open(filename, "w") as fs:
        writer = csv.writer(fs)
        writer.writerow(["link", "username", "count_comment"])
    loop = asyncio.get_event_loop()
    tasks = loop.run_until_complete(asyncio.gather(*(get_text(link) for link in links)))
    loop.close()
    for i in range(len(tasks)):
        soup = BeautifulSoup(tasks[i][0], "html.parser")
        comments = soup.find_all("div", class_="comment")
        usernames = []
        for item in comments:
            user = item.find("a", class_="user-info user-info_inline")
            if user is not None:
                usernames.append(user["data-user-login"])
        write_to_file(filename, tasks[i][1], Counter(usernames))


if __name__ == '__main__':
    filename = 'top_user_comments.csv'
    links = sys.argv[1:4]

    main(filename, links)
