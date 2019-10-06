#!/usr/bin/env python
# coding: utf-8

from heapq import nlargest
from heapq import merge


class User:
    def __init__(self, user_id):
        self._following = []
        self._posted = []


class Post:
    def __init__(self, post_id):
        self._views = []


class VKPoster:

    def __init__(self):
        self._users = {}
        self._posts = {}

    def _check_user(self, user_id):
        if user_id not in self._users:
            self._users[user_id] = User(user_id)

    def _check_post(self, post_id):
        if post_id not in self._posts:
            self._posts[post_id] = Post(post_id)

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        self._check_user(user_id)
        self._check_post(post_id)
        self._users[user_id]._posted.append(post_id)

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        self._check_user(user_id)
        self._check_post(post_id)
        if user_id not in self._posts[post_id]._views:
            self._posts[post_id]._views.append(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        self._check_user(followee_user_id)
        self._check_user(follower_user_id)
        self._users[follower_user_id]._following.append(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int) -> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        tmp = merge(
            *[self._users[user]._posted for user in
                self._users[user_id]._following])
        return nlargest(k, tmp)

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        tmp = nlargest(k, self._posts, key=lambda post_id: [
                       len(self._posts[post_id]._views), post_id])
        return tmp
