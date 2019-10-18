import sys
import requests
import csv
import asyncio
from threading import Thread
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from aiohttp import client_exceptions


def sync_go_to_web(link, all_responses, i):
    try:
        response = requests.get(link)
        del all_responses[i]
        all_responses.insert(i, response.text)
    except requests.exceptions.RequestException as e:
        print(e)


async def fetch(url, session):
    try:
        async with session.get(url) as response:
            return await response.text()
    except (client_exceptions.ClientConnectorError,
            client_exceptions.InvalidURL) as e:
        print(e)


async def run(links):
    tasks = []
    async with ClientSession() as session:
        for link in links:
            task = asyncio.ensure_future(fetch(link, session))
            if task:
                tasks.append(task)
        responses = await asyncio.gather(*tasks)
    return responses


def main(filename, links, type_of_going_to_web='async'):
    if type_of_going_to_web == 'sync':
        all_responses = [None for _ in range(3)]
        threads = []
        for i, link in enumerate(links):
            thread = Thread(target=sync_go_to_web, args=(link,
                                                         all_responses, i))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
    elif type_of_going_to_web == 'async':
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(run(links))
        all_responses = loop.run_until_complete(future)
    result_lst_of_lst = []
    with open(filename, 'w', newline='') as file_:
        writer = csv.writer(file_)
        writer.writerows([['link', 'username', 'count_comment']])
    for i, response in enumerate(all_responses):
        if response:
            soup = BeautifulSoup(response, "html.parser")
            substring = ("user-info__nickname user-info__nickname_small " +
                         "user-info__nickname_comment")
            nicknames = soup.find_all("span", attrs={"class": [substring]})
            result_dict = {}
            for nick in nicknames:
                if nick.text in result_dict:
                    result_dict[nick.text] += 1
                else:
                    result_dict[nick.text] = 1
            for nick, count_comment in result_dict.items():
                result_lst_of_lst.append([links[i], nick, count_comment])
        result_lst_of_lst = sorted(result_lst_of_lst, key=lambda lst: (
                                              lst[0], -lst[2]))
    with open(filename, 'a', newline='') as file_:
        writer = csv.writer(file_)
        writer.writerows(result_lst_of_lst)


if __name__ == '__main__':
    filename = 'top_user_comments.csv'
    links = sys.argv[1:4]
    main(filename, links)
