#!/usr/bin/env python
# coding: utf-8
from queue import PriorityQueue


class VKPoster:
    class Post:
        def __init__(self, post_id):
            self.post_id = post_id
            self.users_read = set()

    class User:
        def __init__(self, user_id):
            self.user_id = user_id
            self.posts = []
            self.follows = set()

    def __init__(self):
        self.users = {}
        self.posts = {}

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self.users:
            self.users[user_id] = self.User(user_id)
        self.users[user_id].posts.append(post_id)
        self.posts[post_id] = self.Post(post_id)

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self.users:
            self.users[user_id] = self.User(user_id)
        if post_id not in self.posts:
            self.posts[post_id] = self.Post(post_id)
        self.posts[post_id].users_read.add(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id not in self.users:
            self.users[follower_user_id] = self.User(follower_user_id)
        if followee_user_id not in self.users:
            self.users[followee_user_id] = self.User(followee_user_id)
        self.users[follower_user_id].follows.add(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int)-> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        if user_id not in self.users:
            self.users[user_id] = self.User(user_id)
        posts = []
        for follow_id in self.users[user_id].follows:
            posts += self.users[follow_id].posts[-k:]
        posts.sort()
        return posts[-k:][::-1]

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        queue = PriorityQueue()
        popular_posts = []
        for post in self.posts.values():
            queue.put(((-len(post.users_read), -post.post_id), post.post_id))
        for _ in range(k):
            if queue.empty():
                return popular_posts
            post_id = queue.get()[1]
            popular_posts.append(post_id)
        return popular_posts
