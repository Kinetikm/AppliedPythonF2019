import csv

from homeworks.homework_05_web.get_top_user_comments import main


def test_top_user_comments():
    filename = '/tmp/test_top_user_comments.csv'
    links = [
        'http://localhost/',
    ]

    try:
        main(filename, links)
    except NotImplementedError:
        return True

    open(filename, 'a').close()
    with open(filename) as f:
        reader = csv.reader(f)
        assert list(reader) == [['link', 'username', 'count_comment']]
