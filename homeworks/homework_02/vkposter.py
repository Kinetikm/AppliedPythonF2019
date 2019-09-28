#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.users = {}
        self.posts = {}
        self.all_posts = []

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self.users:
            self.users[user_id] = set()
        self.posts[post_id] = [set(), user_id]
        self.all_posts.append(post_id)

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self.users:
            self.users[user_id] = set()
        if post_id not in self.posts:
            self.posts[post_id] = [set(), None]
            self.all_posts.append(post_id)
        self.posts[post_id][0].add(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if followee_user_id not in self.users:
            self.users[followee_user_id] = set()
        if follower_user_id not in self.users:
            self.users[follower_user_id] = set()
        self.users[follower_user_id].add(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int) -> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        if user_id not in self.users:
            self.users[user_id] = set()
        fresh_posts = []
        for post_id in sorted((self.all_posts), reverse=True):
            if self.posts[post_id][1] in self.users[user_id]:
                fresh_posts.append(post_id)
                k -= 1
                if k == 0:
                    return fresh_posts
        return fresh_posts

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все
        время, остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        popularity = []
        for post_id in self.all_posts:
            popularity.append(len(self.posts[post_id][0]))
        popularity_and_post = zip(popularity, self.all_posts)
        most_popular_posts_s = sorted(popularity_and_post, key=lambda
                                      point: (point[0], point[1]),
                                      reverse=True)
        most_popular_posts = [post[1] for post in most_popular_posts_s]
        return most_popular_posts[:k]
