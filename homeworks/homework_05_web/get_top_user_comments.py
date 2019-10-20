import sys
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ProcessPoolExecutor
from functools import partial
import pandas as pd


def link_parser(our_dict, link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "html.parser")
    for i in soup.findAll("a", attrs={"class": ["user-info user-info_inline"]}):
        if our_dict.get((i['data-user-login'], link)) is None:
            our_dict[(i['data-user-login'], link)] = 1
        else:
            our_dict[(i['data-user-login'], link)] += 1
    return our_dict


def main(links, filename):
    our_dict = {}
    func = partial(link_parser, our_dict)
    with ProcessPoolExecutor(max_workers=len(links)) as executor:
        for i in executor.map(func, links):
            our_dict = {**our_dict, **i}
    df = pd.DataFrame([[i[1], i[0], our_dict[i]] for i in our_dict])
    df.sort_values(by=[df.columns[0], df.columns[2], df.columns[1]], ascending=False, inplace=True)
    df.to_csv('top_user_comments.csv', index=False, header=False)


if __name__ == '__main__':
    filename = 'top_user_comments.csv'
    links = sys.argv[1:4]
    main(links, filename)
