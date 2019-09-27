#!/usr/bin/env python
# coding: utf-8

import heapq


class VKPoster:

    def __init__(self):
        self.users = dict()  # dict с id пользователей где self.users[user_id] =  {'posts': [], 'subs': []}
        self.views = dict()  # dict с id пол-й где self.views[post_id] = {№ просмотров, id юзеров просмотревшие пост}

    def user_posted_post(self, user_id, post_id):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self.users:
            self.users[user_id] = {'posts': [], 'subs': []}
        self.users[user_id]['posts'].append(post_id)

    def user_read_post(self, user_id, post_id):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if post_id not in self.views:
            self.views[post_id] = [1, [user_id]]
        else:
            if user_id not in self.views[post_id][1]:
                self.views[post_id][0] += 1
                self.views[post_id][1].append(user_id)

    def user_follow_for(self, follower_user_id, followee_user_id):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id not in self.users:
            self.users[follower_user_id] = {'posts': [], 'subs': []}
        if followee_user_id not in self.users:
            self.users[followee_user_id] = {'posts': [], 'subs': []}
        self.users[follower_user_id]['subs'].append(followee_user_id)

    def get_recent_posts(self, user_id, k):
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        list = []
        for i in range(len(self.users[user_id]['subs'])):
            id_sub = self.users[user_id]['subs'][i]
            list += self.users[id_sub]['posts']
        list.sort(reverse=True)
        return list[:k]

    def get_most_popular_posts(self, k):
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        p = []
        for key, val[0] in self.views.items():
            heapq.heappush(p, (val, key))
        return [m[1] for m in heapq.nlargest(k, p)]
