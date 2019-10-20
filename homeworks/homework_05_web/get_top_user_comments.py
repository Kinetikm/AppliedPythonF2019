import sys
import requests
from bs4 import BeautifulSoup
from multiprocessing import Manager, Pool
import csv


def get_resp(link):
    try:
        resp = requests.get(link)
        return resp
    except requests.exceptions.ConnectionError:
        print("Cant open link {}".format(link))


def user_comments(link, link_dict):
    users_dict = {}
    resp = get_resp(link)
    if resp == None:
    	return
    soup = BeautifulSoup(resp.text, "html.parser")
    comments = soup.find_all("a", class_="user-info user-info_inline")
    for comment in comments:
        user = comment.attrs["data-user-login"]
        if user in users_dict:
            users_dict[user] += 1
        else:
            users_dict[user] = 1
    link_dict[link] = sorted(users_dict.items(), key=lambda k: k[1], reverse=True)


def main(filename, links):
    proc_num = 3
    pool = Pool(proc_num)
    procs = []
    link_dict = Manager().dict()

    for link in links:
        proc = pool.apply_async(user_comments, (link, link_dict,))
        procs.append(proc)
    for proc in procs:
        proc.get()

    with open(filename, mode='w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['link', 'username', 'count_comment'])
        for link, user in sorted(link_dict.items(), key=lambda k: k[0], reverse=True):
            for username, num in user:
                writer.writerow([link, username, num])

if __name__ == '__main__':
    filename = 'top_user_comments.csv'
    links = sys.argv[1:4]

    main(filename, links)
