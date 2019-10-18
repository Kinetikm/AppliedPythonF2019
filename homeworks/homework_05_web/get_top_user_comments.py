import sys


import requests
from bs4 import BeautifulSoup
from multiprocessing import Process, Manager


def count_comments(link, users_dict):
    users = {}
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")

    comments = soup.find_all("div", attrs={"class": ["comment"]})
    for comment in comments:
        try:
            user = comment.find('a')["data-user-login"]
            if user not in users:
                users[user] = 1
            else:
                users[user] += 1
        except TypeError:
            pass
    users_dict[link] = users


def main(filename, links):
    procs = []
    manager = Manager()
    users_dict = manager.dict()
    for link in links:
        proc = Process(target=count_comments, args=(link, users_dict, ))
        procs.append(proc)
        proc.start()
    for proc in procs:
        proc.join()
    with open(filename, 'w') as f:
        while len(users_dict) != 0:
            first = min(users_dict.keys())
            for item in reversed(sorted(users_dict[first].items(), key = lambda x: x[1])):
                f.write(str(first) + ', ' + str(item[0]) + ', ' + str(item[1])+ '\n')
            del users_dict[first]

if __name__ == '__main__':
    filename = 'top_user_comments.csv'    # doc where result will be stored
    links = sys.argv[1:4]    # arguments is 3 links to habr articles
    main(filename, links)
