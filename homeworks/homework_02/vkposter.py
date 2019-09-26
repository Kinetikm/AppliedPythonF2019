#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.user_post = {}
        self.user_follow = {}
        self.read_post = {}

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if (user_id in self.user_post):
            self.user_post[user_id].append(post_id)
        else:
            self.user_post[user_id] = [post_id]

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if post_id in self.read_post:
            if user_id not in self.read_post[post_id]['marked']:
                self.read_post[post_id]['cnt'] += 1
                self.read_post[post_id]['marked'].append(user_id)
        else:
            self.read_post[post_id] = {'cnt': 1, 'marked': [user_id]}

    def user_follow_for(self, flwr: int, flwe: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if flwr != flwe:
            if flwr in self.user_follow:
                self.user_follow[flwr].append(flwe)
            else:
                self.user_follow[flwr] = [flwe]

    def get_recent_posts(self, user_id: int, k: int)-> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        result = []
        for i in self.user_follow[user_id]:
            if i in self.user_post:
                result.extend(self.user_post[i])
        return sorted(result, reverse=True)[:k]

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        return sorted(self.read_post.keys(), key=lambda x: (self.read_post[x]['cnt'], x), reverse=1)[:k]
