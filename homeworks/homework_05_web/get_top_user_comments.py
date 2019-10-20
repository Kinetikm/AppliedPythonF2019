import sys
import csv
import aiohttp
import asyncio
from bs4 import BeautifulSoup


def write_csv_if_file(lines, filename):
    with open(filename, 'w') as f:
        comment_writer = csv.writer(f, delimiter=',')
        comment_writer.writerow(['link', 'username', 'count_comment'])
        lines = sorted(lines, key=lambda row: (row[0], row[2]))
        for line in lines:
            comment_writer.writerow([*line])


async def parse_http(text):
    count = {}
    soup = BeautifulSoup(text, "html.parser")
    users = soup.findAll('a', attrs={'class': ["user-info user-info_inline"]})

    for user in users:
        login = user["data-user-login"]
        if login not in count:
            count[login] = 1
        else:
            count[login] += 1

    return count


async def get_count_comment(link, lines):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                count = await parse_http(await resp.text())
                lines += [(link, row[0], row[1]) for row in count.items()]
    except:
        return

def main(filename, links):
    ioloop = asyncio.get_event_loop()
    lines_for_writing, tasks = [], []

    for link in links:
        tasks.append(ioloop.create_task(get_count_comment(link, lines_for_writing)))

    ioloop.run_until_complete(asyncio.wait(tasks))
    ioloop.close()

    write_csv_if_file(lines_for_writing, filename)


if __name__ == '__main__':
    filename = 'top_user_comments.csv'
    links = sys.argv[1:4]
    main(filename, links)
