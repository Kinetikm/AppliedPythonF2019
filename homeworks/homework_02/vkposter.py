# !/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.user_posts = {}
        self.user_follow = {}
        self.users_like_posts = {}

    def user_posted_post(self, user_id, post_id):
        """
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        """
        if user_id not in self.user_posts:
            self.user_posts[user_id] = [post_id]
        else:
            self.user_posts[user_id].append(post_id)

    def user_read_post(self, user_id, post_id):
        """
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        """
        if post_id not in self.users_like_posts:
            self.users_like_posts[post_id] = []
        if user_id not in self.users_like_posts[post_id]:
            self.users_like_posts[post_id].append(user_id)

    def user_follow_for(self, follower_user_id, followee_user_id):
        """
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        """
        if follower_user_id not in self.user_follow:
            self.user_follow[follower_user_id] = []
        self.user_follow[follower_user_id].append(followee_user_id)

    def get_recent_posts(self, user_id, k):
        """
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        """
        posts = []
        for id in self.user_follow[user_id]:
            if id in self.user_posts:
                posts += self.user_posts[id]
        posts.sort()
        posts = posts[::-1]
        return posts[:k:]

    def get_most_popular_posts(self, k):
        """
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        """
        posts = list(self.users_like_posts.items())
        posts.sort(key=lambda parameter_sort: (
            len(parameter_sort[1]),
            parameter_sort[0]))
        posts = posts[::-1]
        posts = posts[:k:]
        return [x[0] for x in posts]
