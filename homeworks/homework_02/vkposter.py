#!/usr/bin/env python
# coding: utf-8


from homeworks.homework_02.heap import MaxHeap
from homeworks.homework_02.fastmerger import FastSortedListMerger


class VKPoster:

    def __init__(self):
        self.user_post = {}
        self.user_subs = {}
        self.post_watched = {}

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id in self.user_post:
            self.user_post[user_id].insert(0, post_id)
        else:
            self.user_post[user_id] = [post_id]
        pass

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if post_id in self.post_watched:
            if user_id not in self.post_watched[post_id]:
                self.post_watched[post_id].append(user_id)
        else:
            self.post_watched[post_id] = [user_id]
        pass

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id in self.user_subs:
            if followee_user_id not in self.user_subs[follower_user_id]:
                self.user_subs[follower_user_id].append(followee_user_id)
        else:
            self.user_subs[follower_user_id] = [followee_user_id]
        pass

    def get_recent_posts(self, user_id: int, k: int)-> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        posts = []
        if user_id in self.user_subs:
            for sub in self.user_subs[user_id]:
                    if sub in self.user_post:
                        posts = posts + self.user_post[sub]
            for post in posts:
                if post in self.post_watched:
                    if user_id in self.post_watched[post]:
                        posts.remove(post)
            posts.sort(reverse=True)
        return posts[:k]
        pass

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        posts = self.post_watched.copy()
        for key in posts:
            posts[key] = len(posts[key])
        views = sorted(set(posts.values()), reverse=True)
        out = {}
        for view in views:
            out[view] = []
            for post in posts:
                if posts[post] == view:
                    out[view].append(post)
                    out[view].sort(reverse=True)
        result = []
        for key in out:
            result = result + out[key]
        if len(result) >= k:
            return result[:k]
        pass