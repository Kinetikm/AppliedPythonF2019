import sys
import urllib

import requests
from bs4 import BeautifulSoup


def opener(link):
    response = requests.get(link)
    if response is not None:
        html = BeautifulSoup(response.text, 'html.parser')
        names = {}

        comments = html.find_all("span", attrs={"class": [
            "user-info__nickname user-info__nickname_small "
            "user-info__nickname_comment"]})

        for comment in comments:
            if comment.text in names:
                names[comment.text] = names[comment.text] + 1
            else:
                names[comment.text] = 1

        return sorted(names.items(), key=lambda kv: kv[1])


def main(filename, links):
    for ind, link in enumerate(links):
        result = opener(link)
        if ind == 0:
            with open(filename, 'w') as file:
                for keys in result:
                    file.write("{}, {}, {}\n".format(link, keys[0], keys[1]))
        else:
            with open(filename, 'a') as file:
                for keys in result:
                    file.write("{}, {}, {}\n".format(link, keys[0], keys[1]))


if __name__ == '__main__':
    filename = 'top_user_comments.csv'
    links = sys.argv[1:4]

    main(filename, links)
