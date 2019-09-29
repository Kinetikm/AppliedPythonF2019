#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.post = {}
        self.read = {}
        self.watched = {}

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self.post:
            self.post[user_id] = {0: [], 1: []}
        self.post[user_id][0].append(post_id)

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if post_id not in self.watched:
            self.watched[post_id] = []
            self.read[post_id] = 0
        if user_id not in self.watched[post_id]:
            self.watched[post_id].append(user_id)
            self.read[post_id] += 1

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id not in self.post:
            self.post[follower_user_id] = {0: [], 1: []}
        self.post[follower_user_id][1].append(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int)-> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        a = list()
        for user in self.post[user_id][1]:
            a += self.post[user][0]
        a = sorted(a, reverse=True)
        return a[:k]

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        b = list()
        r = list(self.read.items())
        r.sort()
        r.sort(key=lambda i: i[1])
        r = r[::-1]
        for i in range(0, k, 1):
            b.append(r[i][0])
        return b
