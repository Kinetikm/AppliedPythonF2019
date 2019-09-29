#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        # каждому user_id соответствует словарь,
        # в котором 'followed' - список подписок пользователя
        # и 'posts' - список постов пользователя
        # self.users = {user_id: {'followed': [user_ids], 'posts': [post_ids]}, ...}
        self.users = {}

        # каждому post_id соответствует set(),
        # который состоит id просмотревших этот пост пользователей
        # self.posts = {post_id: set(user_ids), ...}
        self.posts = {}

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        self.posts[post_id] = set()
        self.users.setdefault(user_id, {'followed': [], 'posts': []})['posts'].append(post_id)

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        self.posts.setdefault(post_id, set()).add(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        self.users.setdefault(follower_user_id, {'followed': [], 'posts': []})['followed'].append(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int)-> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        posts_by_followed = []
        for followed_id in self.users[user_id]['followed']:
            posts_by_followed += self.users[followed_id]['posts']

        return sorted(posts_by_followed, reverse=True)[:k]

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        return sorted(self.posts, key=lambda post_id: (len(self.posts[post_id]), post_id), reverse=True)[:k]
