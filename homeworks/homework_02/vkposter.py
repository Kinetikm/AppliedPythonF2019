#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.user_follows = {}  # user id -> ids of user's follows
        self.post_read = {}  # post id -> set user ids
        self.user_posts = {}  # user id -> set user's posts

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id in self.user_posts:
            self.user_posts[user_id].add(post_id)
        else:
            self.user_posts[user_id] = {post_id}
        self.post_read[post_id] = set()

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if post_id in self.post_read:
            self.post_read[post_id].add(user_id)
        else:
            self.post_read[post_id] = {user_id}

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id in self.user_follows:
            self.user_follows[follower_user_id].add(followee_user_id)
        else:
            self.user_follows[follower_user_id] = {followee_user_id}

    def get_recent_posts(self, user_id: int, k: int) -> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        posts = []
        for f in self.user_follows[user_id]:
            if f not in self.user_posts:
                continue
            for f_post in self.user_posts[f]:
                if user_id not in self.post_read[f_post]:
                    posts.append(f_post)
        if len(posts) > k:
            return sorted(posts, reverse=True)[:k]
        else:
            return sorted(posts, reverse=True)

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        res = []
        d = {}  # number of views - post id
        for post in self.post_read:
            n = len(self.post_read[post])
            if n not in d:
                d[n] = []
            d[n].append(post)
        keys_list = sorted(d, reverse=True)
        for key in keys_list:
            d[key].sort(reverse=True)
            res += d[key]
        if len(res) > k:
            res = res[:k]
            return res
