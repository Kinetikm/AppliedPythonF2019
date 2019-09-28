#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self._user_follows = dict()  # user id - his followee ids
        self._user_posts = dict()    # user id - his post ids
        self._post_read = dict()     # post id - user ids (who read)

    def user_posted_post(self, user_id: int, post_id: int):
        """
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        """
        if self._user_posts.get(user_id) is None:
            self._user_posts[user_id] = set()
        self._user_posts[user_id].add(post_id)
        if self._post_read.get(post_id) is None:
            self._post_read[post_id] = set()

    def user_read_post(self, user_id: int, post_id: int):
        """
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        """
        if self._post_read.get(post_id) is None:
            self._post_read[post_id] = set()
        self._post_read[post_id].add(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        """
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        """
        if self._user_follows.get(follower_user_id) is None:
            self._user_follows[follower_user_id] = set()
        self._user_follows[follower_user_id].add(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int) -> list:
        """
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        """
        result = []
        for followee_id in self._user_follows[user_id]:
            if self._user_posts.get(followee_id) is None:
                continue
            for followee_post_id in self._user_posts[followee_id]:
                if followee_post_id not in self._post_read:
                    continue
                if user_id not in self._post_read[followee_post_id]:
                    result.append(followee_post_id)
        result.sort(reverse=True)
        return result[:k] if len(result) > k else result

    def get_most_popular_posts(self, k: int) -> list:
        """
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        """
        post_read = dict()
        for post_id, user_id_list in self._post_read.items():
            been_read = len(user_id_list)
            if post_read.get(been_read) is None:
                post_read[been_read] = []
            post_read[been_read].append(post_id)
        result = []
        keys = sorted(post_read.keys(), reverse=True)
        if len(keys) > k:
            keys = keys[:k]
        for key in keys:
            post_read[key].sort(reverse=True)
            result += post_read[key]
        return result[:k] if len(result) > k else result
