#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.follower_dict = {}
        self.post_read_dict = {}
        self.posted_dict = {}

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self.posted_dict:
            self.posted_dict[user_id] = [post_id]
        else:
            self.posted_dict[user_id].append(post_id)

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self.post_read_dict:
            self.post_read_dict[user_id] = [post_id]
        else:
            if not post_id in self.post_read_dict[user_id]:
                self.post_read_dict[user_id].append(post_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id not in self.follower_dict:
            self.follower_dict[follower_user_id] = [followee_user_id]
        else:
            self.follower_dict[follower_user_id].append(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int) -> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        if user_id in self.follower_dict:
            follows = self.follower_dict[user_id]
        else:
            follows = []

        posts = []
        for follow in follows:
            if follow in self.posted_dict:
                posts += self.posted_dict[follow]

        posts.sort()

        fresh_posts = posts[-k:]
        fresh_posts.reverse()
        return fresh_posts

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        all_posts = {}

        for user, posts in self.posted_dict.items():
            for post in posts:
                all_posts[post] = 0

        for user, read_posts in self.post_read_dict.items():
            for read_post in read_posts:
                all_posts[read_post] = 0

        for user, read_posts in self.post_read_dict.items():
            for read_post in read_posts:
                all_posts[read_post] += 1

        all_posts_list = []

        for post, popular in all_posts.items():
            all_posts_list.append([post, popular])

        all_posts_list = sorted(all_posts_list)
        all_posts_list = sorted(all_posts_list, key=lambda elem: elem[1])

        all_posts_list = [x[0] for x in all_posts_list]

        fresh_posts = all_posts_list[-k:]
        fresh_posts.reverse()
        return fresh_posts
