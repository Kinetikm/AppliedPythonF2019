#!/usr/bin/env python
# coding: utf-8
import operator


class Post:
    def __init__(self, post_id):
        self.post_id = post_id
        self.popularity = 0
        self.read_by = []

    def inc_popularity(self):
        self.popularity += 1

    def set_read_by(self, user):
        self.read_by.append(user.user_id)


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.created_posts = []
        self.subscriptions = []

    def set_created_posts(self, post):
        self.created_posts.append(post)

    def set_subscription(self, sub_user):
        self.subscriptions.append(sub_user)

    def get_post_subscriptions(self) -> list:
        list_post = []
        for user in self.subscriptions:
            list_post.extend(user.created_posts)

        return list(list_post)


class VKPoster:
    def __init__(self):
        self.users = {}
        self.posts = {}

    def user_posted_post(self, user_id: int, post_id: int):
        """
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        """

        if user_id not in self.users:
            self.users[user_id] = User(user_id)

        if post_id not in self.posts:
            self.posts[post_id] = Post(post_id)

        self.users[user_id].set_created_posts(self.posts[post_id])

    def user_read_post(self, user_id: int, post_id: int):
        """
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        """

        if user_id not in self.users:
            self.users[user_id] = User(user_id)

        if post_id not in self.posts:
            self.posts[post_id] = Post(post_id)

        if user_id not in self.posts[post_id].read_by:
            self.posts[post_id].inc_popularity()
            self.posts[post_id].read_by.append(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        """
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        """

        if follower_user_id not in self.users:
            self.users[follower_user_id] = User(follower_user_id)

        if followee_user_id not in self.users:
            self.users[followee_user_id] = User(followee_user_id)

        self.users[follower_user_id].set_subscription(self.users[followee_user_id])

    def get_recent_posts(self, user_id: int, k: int) -> list:
        """
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        """
        posts = self.users[user_id].get_post_subscriptions()

        # if k > len(posts):
        #     # Выдать ошибку запроса, либо предупреждение

        if user_id in self.users:
            sort_posts_list = sorted(
                posts, key=operator.attrgetter("post_id"), reverse=True
            )[:k]

            return [post.post_id for post in sort_posts_list]

    def get_most_popular_posts(self, k: int) -> list:
        """
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        """
        posts = self.posts.values()

        # if k > len(posts):
        #     # Выдать ошибку запроса, либо предупреждение

        sort_posts_list = sorted(
            posts, key=operator.attrgetter("popularity", "post_id"), reverse=True
        )[:k]

        return [post.post_id for post in sort_posts_list]
