import sys
import requests
import csv
from bs4 import BeautifulSoup


def request(link):
    try:
        req = requests.get(link)
        return req.text
    except requests.exceptions.RequestException:
        return


def parse(text):
    users_comms = {}
    soup = BeautifulSoup(text, 'html.parser')
    comm_num = int(soup.find('span', class_='comments-section__head-counter').text)
    if comm_num < 100:
        return None
    comms = soup.findAll('div', class_='comment__head')
    for comm in comms:
        user = (comm.find('a', class_='user-info user-info_inline').get('data-user-login'))
        if user not in users_comms:
            users_comms[user] = 1
        else:
            users_comms[user] += 1
    return users_comms


def write_csv(filename, rows):
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['link', 'username', 'count_comment'])
        writer.writerows(rows)


def make_rows(link):
    rows = []
    html = request(link)
    if html:
        users_comms = parse(html)
        for key, value in users_comms.items():
            rows.append((link, key, value))
        return rows


def sort_rows(rows):
    rows.sort(key=lambda x: (x[0], -x[2]))
    return rows


def main(filename, links):
    all_rows = []
    for link in links:
        rows = make_rows(link)
        if rows:
            all_rows.extend(rows)
    write_csv(filename, sort_rows(all_rows))


if __name__ == '__main__':
    filename = 'top_user_comments.csv'
    links = sys.argv[1:4]

    main(filename, links)
