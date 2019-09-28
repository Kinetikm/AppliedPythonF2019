#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.posts = dict()
        self.viewers = dict()
        self.views = dict()
        self.subscriptions = dict()

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id in self.posts:
            self.posts[user_id].append(post_id)
        else:
            self.posts[user_id] = [post_id]

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if post_id in self.viewers:
            # если это условие выполняется, то
            # условие (if post_id in self.views)
            # тоже выполняется, так как
            # self.views и self.viewers заполняются
            # синхронно и имеют одинаковые ключи
            self.viewers[post_id].add(user_id)
            self.views[post_id] = len(self.viewers[post_id])
        else:
            self.viewers[post_id] = set()
            self.viewers[post_id].add(user_id)
            self.views[post_id] = len(self.viewers[post_id])

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id in self.subscriptions:
            self.subscriptions[follower_user_id].append(followee_user_id)
        else:
            self.subscriptions[follower_user_id] = [followee_user_id]

    def get_recent_posts(self, user_id: int, k: int)-> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        if user_id not in self.subscriptions:
            return None
        lst = list()
        for cur in self.subscriptions[user_id]:
            if cur not in self.posts:
                # если у текущего пользователя (cur), на которого
                # подписан user_id, нет постов
                continue
            lst += self.posts[cur]
        lst.sort(reverse=True)
        return lst[:k]

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        lst = list(self.views.items())
        lst.sort(key=lambda i: i[1])
        lst.sort(key=lambda i: i[1], reverse=True)
        for i in range(len(lst)):
            lst[i] = lst[i][0]
        lst = lst[:k]
        return lst
