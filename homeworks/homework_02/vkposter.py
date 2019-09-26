#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.posts = {}
        self.users = {}

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self.users:
            self.users[user_id] = (set(), set())
        if post_id not in self.posts:
            self.posts[post_id] = (user_id, set())

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self.users:
            self.users[user_id] = (set(), set())
        if post_id not in self.posts:
            self.posts[post_id] = (None, set())
        self.posts[post_id][1].add(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if followee_user_id not in self.users:
            self.users[followee_user_id] = (set(), set())
        if follower_user_id not in self.users:
            self.users[follower_user_id] = (set(), set())
        self.users[follower_user_id][1].add(followee_user_id)
        self.users[followee_user_id][0].add(follower_user_id)

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
        for key in self.posts:
            if self.posts[key][0] in self.users[user_id][1]:
                posts.append(key)
        return [] if len(posts) == 0 else sorted(posts, reverse=True)[:k if k < len(posts) else len(posts):]

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        sorted_posts = sorted(self.posts.items(), key=lambda post: (len(post[1][1]), post[0]), reverse=True)
        retval = []
        for i in range(k):
            retval.append(sorted_posts[i][0])
        return retval
