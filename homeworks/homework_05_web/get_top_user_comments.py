import sys
import requests
import csv
from threading import Thread
from bs4 import BeautifulSoup


def go_to_web(link, all_responses):
    try:
        response = requests.get(link)
        all_responses.append(response)
    except requests.exceptions.RequestException as e:
        print(e)


def main(filename, links):
    all_responses = []
    threads = []
    for link in links:
        thread = Thread(target=go_to_web, args=(link, all_responses))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    result_lst_of_lst = [['link', 'username', 'count_comment']]
    for response in all_responses:
        soup = BeautifulSoup(response.text, "html.parser")
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
            result_lst_of_lst.append([response.url, nick, count_comment])
    result_lst_of_lst = sorted(result_lst_of_lst, key=lambda lst: (
                                          lst[0], lst[2]), reverse=True)
    with open(filename, 'w', newline='') as file_:
        writer = csv.writer(file_)
        writer.writerows(result_lst_of_lst)


if __name__ == '__main__':
    filename = 'top_user_comments.csv'
    links = sys.argv[1:4]
    # links = ['https://habr.com/ru/company/habr/blog/443222/',
    #         'https://habr.com/ru/post/124363/',
    #         'https://habr.com/ru/post/448530/']
    main(filename, links)
