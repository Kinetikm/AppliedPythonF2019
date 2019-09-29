#!/usr/bin/env python
# coding: utf-8


# from homeworks.homework_02.heap import MaxHeap
# from homeworks.homework_02.fastmerger import FastSortedListMerger


class VKPoster:

    def __init__(self):
        self._users = {}
        self._posts = {}
        '''
        Словарь типа {user_id: {dict}}
            dict типа {'posts':[], 'follows":[]}
                posts - посты, опубликованные юзером
                    posts dict - словарь постов, ключ - id поста, значение - список из id просмотревших людей
                follows - список юзеров, на которых подписан данный человек
        posts: словарь
            {post_id: []}, [] - список просмотревших юзеров
        '''

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self._users:
            self._users[user_id] = {'posts': [], 'follows': []}
        self._users[user_id]['posts'].append(post_id)
        self._posts[post_id] = []

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self._users:
            self._users[user_id] = {'posts': [], 'follows': []}
        if user_id not in self._posts[post_id]:
            self._posts[post_id].append(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id not in self._users:
            self._users[follower_user_id] = {'posts': [], 'follows': []}
        if followee_user_id not in self._users:
            self._users[followee_user_id] = {'posts': [], 'follows': []}
        self._users[follower_user_id][follows].append(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int) -> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        ans = []

        for followee in self._users[user_id]['follows']:
            for post in self._users[followee]['posts']:
                ans.append(post)
        return sorted(ans, reverse=True)[:k] if k > len(ans) else sorted(ans, reverse=True)


    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        ans = sorted(self._posts, key=lambda x: len(self._posts[x]), reverse=True)
        return ans[:k] if k > len(ans) else ans
