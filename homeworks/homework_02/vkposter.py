#!/usr/bin/env python
# coding: utf-8


from homeworks.homework_02.heap import MaxHeap
from homeworks.homework_02.fastmerger import FastSortedListMerger


class VKPoster:

    users = dict()  # key = user_id; value = User

    def __init__(self):
        pass

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        self.users[user_id].new_post(post_id)

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        self.users[user_id].new_read(post_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        self.users[follower_user_id].new_subscribe(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int)-> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        new_posts = []
        for user in self.users[user_id].subscribes:
            for post_id in user.posts:
                new_posts.append(post_id)
        new_posts = sorted(new_posts, reverse=True)
        return new_posts[0:k:]


    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        posts = dict()
        for user in self.users.values():
            for post_id in user.posts:
                if not (post_id in posts.keys()):
                    posts[post_id] = 1
                else:
                    posts[post_id] += 1
        list_posts = list(posts.items())
        list_posts.sort(key=lambda i: i[1], reverse=True)  # отсортировали по популярности
        list_posts = list_posts[0:k:]
        popular_posts = [posts[post_id] for post_id in list_posts]
        return sorted(popular_posts, reverse=True)


class User():

    posts = []  # post_id
    subscribes = []  # user_id
    read = []  # post_id

    def __init__(self, user_id):
        self.user_id = user_id

    def new_subscribe(self, user_id):
        if not (user_id in self.subscribes):
            self.subscribes.append(user_id)

    def new_post(self, post_id):
        if not (post_id in self.posts):
            self.posts.append(post_id)

    def new_read(self, post_id):
        if not (post_id in self.read):
            self.read.append(post_id)
