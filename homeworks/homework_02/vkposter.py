#!/usr/bin/env python
# coding: utf-8
import heapq


class User:

    def __init__(self):
        """
        posts: list posts id posted by user
        follow: list of user_id which user follows
        followers: list of user_id follows bu user
         """
        self.posts = []
        self.follow = []
        self.followers = []

    def add_post(self, post_id):
        self.posts.append(post_id)

    def follow_by(self, follow_user_id):
        self.follow.append(follow_user_id)

    def add_follower(self, follower_id):
        self.followers.append(follower_id)


class Post:

    def __init__(self):
        """
        readers: set of user_id, which read post
        """
        self.readers = set()

    def readed(self, user_id):
        self.readers.add(user_id)

    def num_reading(self):
        return len(self.readers)


class VKPoster:

    def __init__(self):
        self._users = dict()
        self._posts = dict()

    def user_posted_post(self, user_id: int, post_id: int):
        """
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        """
        if user_id not in self._users:
            self._users[user_id] = User()
        self._users[user_id].add_post(post_id)
        self._posts[post_id] = Post()

    def user_read_post(self, user_id: int, post_id: int):
        """
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        """
        if post_id not in self._posts:
            self._posts[post_id] = Post()
        self._posts[post_id].readed(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        """
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        """
        if followee_user_id not in self._users:
            self._users[followee_user_id] = User()
        if follower_user_id not in self._users:
            self._users[follower_user_id] = User()
        self._users[followee_user_id].add_follower(follower_user_id)
        self._users[follower_user_id].follow_by(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int) -> list:
        """
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        """
        authors = self._users[user_id].follow
        all_posts = []
        for author in authors:
            all_posts += self._users[author].posts
        result = heapq.nlargest(k, all_posts)
        return result

    def get_most_popular_posts(self, k: int) -> list:
        """
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        """
        readings = {}
        for key, value in self._posts.items():
            readings[key] = value.num_reading()
        sorted_readings = sorted(readings.items(), key=lambda x: (x[1], x[0]), reverse=True)
        top = [i[0] for i in sorted_readings[:k]]
        return top
