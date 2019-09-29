#!/usr/bin/env python
# coding: utf-8


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
        if post_id not in self.posts:
            self.posts[post_id] = {'user_id': user_id, 'post_read_users': []}

    def user_read_post(self, user_id: int, post_id: int):
        """
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        """
        if post_id not in self.posts:
            self.posts[post_id] = {'user_id': None, 'post_read_users': []}
        if user_id not in self.posts[post_id]['post_read_users']:
            self.posts[post_id]['post_read_users'].append(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        """
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        """
        if follower_user_id not in self.users:
            self.users[follower_user_id] = []
        self.users[follower_user_id].append(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int) -> list:
        """
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        """
        buff_of_all_posts = list(self.posts.keys())
        buff_of_all_posts.sort(reverse=True)
        buff_of_k_posts = []
        item = 0
        for i in range(len(buff_of_all_posts)):
            if self.posts[buff_of_all_posts[i]]['user_id'] in self.users[user_id]:
                buff_of_k_posts.append(buff_of_all_posts[i])
                item += 1
            if item == k:
                break
        return buff_of_k_posts

    def get_most_popular_posts(self, k: int) -> list:
        """
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        """
        all_posts = []
        buff_of_reads = []
        for key in self.posts:
            all_posts.append(key)
            buff_of_reads.append(len(self.posts[key]['post_read_users']))
        reads_and_posts = zip(buff_of_reads, all_posts)
        buff = [post[1] for post in sorted(reads_and_posts, key=lambda point: (point[0],
                                                                               point[1]), reverse=True)]
        return buff[:k]
