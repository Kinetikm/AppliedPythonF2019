#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.users = {}
        self.posts = {}

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id in self.users:
            self.users[user_id][1].append(post_id)
        else:
            self.users[user_id] = [[], [post_id]]
        self.posts[post_id] = set()

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self.users:
            self.users[user_id] = [[], []]
        if post_id in self.posts:
            self.posts[post_id].add(user_id)
        else:
            self.posts[post_id] = set(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id not in self.users:
            self.users[follower_user_id] = [[], []]
        if followee_user_id not in self.users:
            self.users[followee_user_id] = [[], []]
        self.users[follower_user_id][0].append(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int)-> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        r = []
        l = []
        for i in self.users[user_id][0]:
            l.extend(self.users[i][1])
        l.sort()
        print("l = {}".format(l))
        r = l[len(l):len(l) - k - 1: -1]
        return r

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        r = []
        l = list()
        kl = list()
        kl.extend(self.posts.keys())
        l = [len(self.posts[i]) for i in kl]
        l.sort()
        sr = list()
        l = l[::-1]
        l = l[0:k]
        p = l[k - 1]
        s = set(l)
        s.remove(p)
        kl.sort()
        sl = self.posts.copy()
        for i in kl[::-1]:
            if len(self.posts[i]) in s:
                r.append(i)
                kl.remove(i)
        for i in kl[::-1]:
            if len(r) == k:
                break
            if len(sl[i]) == p:
                r.append(i)
        r.sort()
        r = r[::-1]
        return(r)
