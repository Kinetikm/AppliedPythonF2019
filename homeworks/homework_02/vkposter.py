#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.info = {
            'users': {},
            'posts': {}
        }

    def user_posted_post(self, user_id: int, post_id: int):
        """
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        """
        self.info['posts'][post_id] = {
            'user': user_id,
            'views': []
        }

    def user_read_post(self, user_id: int, post_id: int):
        """
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        """
        if self.info['posts'].get(post_id) is None:
            self.info['posts'][post_id] = {
                'user': None,
                'views': []
            }
        if user_id not in self.info['posts'][post_id]['views']:
            self.info['posts'][post_id]['views'].append(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        """
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        """
        if self.info['users'].get(follower_user_id) is None:
            self.info['users'][follower_user_id] = []
        self.info['users'][follower_user_id].append(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int) -> list:
        """
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        """
        posts = []
        for post in self.info['posts'].keys():
            if self.info['posts'][post]['user'] in self.info['users'][user_id]:
                posts.append(post)
        if len(posts) > k:
            return sorted(posts, reverse=True)[:k]
        return sorted(posts, reverse=True)

    def get_most_popular_posts(self, k: int) -> list:
        """
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        """
        posts = {}
        for post in self.info['posts'].keys():
            if posts.get(post) is None:
                posts[post] = 0
            posts[post] = len(self.info['posts'][post]['views'])
        all_posts = []
        all_posts.extend(posts.items())
        sorted_posts = sorted(all_posts, key=lambda x: (-x[1], -x[0]))
        fresh_posts = []
        for tup in sorted_posts:
            fresh_posts.append(tup[0])
        if len(fresh_posts) > k:
            return fresh_posts[:k]
        return fresh_posts
