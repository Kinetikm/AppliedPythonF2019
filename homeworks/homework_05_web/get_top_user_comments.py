import sys
import requests
from bs4 import BeautifulSoup
import csv


def get_data(link):
    """
    send get request to get data
    :param link: url
    :return: html text
    """
    resp = requests.get(link)
    return resp.text


def pars_comments(data):
    """
    html page parsing
    :param data: html text
    :return: {user: number_of_comments}
    """
    soup = BeautifulSoup(data, 'lxml')
    comments_heads = soup.find_all('div', class_="comment__head ")
    users_comments = {}
    for comment in comments_heads:
        user_info = comment.find('a', class_="user-info user-info_inline")
        user_login = user_info['data-user-login']
        if user_login in users_comments:
            users_comments[user_login] += 1
        else:
            users_comments[user_login] = 1
    return users_comments

def process_link(link):
    page = get_data(link)
    data = pars_comments(page)
    return [(link, key, value) for key, value in data.items()]


def write_csv(file_name, rows):
    """sort and write rows in csv file in format link,username,number_of_comments"""
    rows.sort(key=lambda x: x[2], reverse=True) # Сортируем по количеству коментариев
    rows.sort(key=lambda x: x[0]) # и по ссылкам (у ссылок приоретет выше). Сортировка стабильна, поэтому это работет
    with open(file_name, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(('link','username','count_comment'))
        for row in rows:
            writer.writerow(row)


def main(file_name, urls):
    data = []
    for link in urls:
        data += process_link(link)
    write_csv(file_name, data)


if __name__ == '__main__':
    filename = 'top_user_comments.csv'
    links = sys.argv[1:4]

    main(filename, links)
