#!/usr/bin/env python
# coding: utf-8
from collections import defaultdict


class VKPoster:

    def __init__(self):
        self.all_posts = {}
        self.posts = defaultdict(lambda: {'posts': [], 'followee': []})
        self.read_posts = {}
        pass

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if post_id not in self.posts[user_id]['posts']:
            self.posts[user_id]['posts'].append(post_id)
        if post_id not in self.posts.values():
            self.all_posts[post_id] = [0, post_id]
        pass

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if post_id not in self.read_posts:
            self.read_posts[post_id] = {
                'readers': [user_id],
                'count of reads': 1
            }
        elif user_id not in self.read_posts[post_id]['readers']:
            self.read_posts[post_id]['readers'].append(user_id)
            self.read_posts[post_id]['count of reads'] += 1
        if post_id in self.all_posts:
            self.all_posts[post_id][0] = \
                self.read_posts[post_id]['count of reads']
        else:
            self.all_posts[post_id] = [1, post_id]

        pass

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if followee_user_id not in self.posts[follower_user_id]['followee']:
            self.posts[follower_user_id]['followee'].append(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int) -> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        bb = []
        for i in self.posts[user_id]['followee']:
            if i in self.posts.keys():
                bb += (self.posts[i]['posts'])
        return (sorted(bb, key=lambda c: c, reverse=True)[0:k])

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        c = sorted(self.all_posts.values(), key=lambda c: c, reverse=True)
        print(sorted(c, key=lambda l: l, reverse=True))
        b = []
        for i in range(k):
            b.append(c[i][1])
        return b
        pass
