#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.d = {}
        self.eyes = {}

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self.d:
            self.d[user_id] = {'posts': [], 'followees': []}
        self.d[user_id]['posts'].append(post_id)

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if post_id not in self.eyes:
            self.eyes[post_id] = [1, user_id]
        else:
            if user_id not in self.eyes[post_id][1:]:
                self.eyes[post_id][0] += 1
                self.eyes[post_id].append(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''

        if follower_user_id not in self.d:
            self.d[follower_user_id] = {'posts': [], 'followees': []}
        self.d[follower_user_id]['followees'].append(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int)-> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        arr = []
        for user in self.d[user_id]['followees']:
            arr = arr + self.d[user]['posts']
        arr = sorted(arr, reverse=True)
        return arr[:k]

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        max_id = max(self.eyes)
        f = max_id*[0]
        for id_ in range(1, max_id+1):
            if id_ in self.eyes:
                f[max_id - id_] = self.eyes[id_][0]

        lst = []
        for i in range(k):
            temp = f.index(max(f))
            f[temp] = -1
            lst.append(max_id - temp)

        return lst
