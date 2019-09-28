#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.subscriptions = dict()
        self.posts = list()

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        self.posts.append(
            {"post_id": post_id, "user_id": user_id, "statistic": set()})

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        for post in self.posts:
            if post["post_id"] == post_id:
                post["statistic"].add(user_id)
                return
        self.posts.append(
            {"post_id": post_id, "user_id": "anonym", "statistic": {user_id}})

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id not in self.subscriptions:
            self.subscriptions[follower_user_id] = {followee_user_id}
        else:
            self.subscriptions[follower_user_id].add(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int) -> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        result = list()
        self.posts.sort(key=sort_by_date, reverse=True)
        for post in self.posts:
            if post["user_id"] in self.subscriptions[user_id]:
                result.append(post["post_id"])
                k -= 1
                if k == 0:
                    break
        return result

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        result = []
        self.posts.sort(key=sort_by_date, reverse=True)
        for post in sorted(self.posts, key=sort_by_len, reverse=True):
            result.append(post["post_id"])
            k -= 1
            if k == 0:
                break
        return result


def sort_by_len(el):
    return len(el["statistic"])


def sort_by_date(el):
    return el["post_id"]
