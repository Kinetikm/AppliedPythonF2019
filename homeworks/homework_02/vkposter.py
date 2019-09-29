#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.pp = dict()
        self.pr = dict()
        self.pf = dict()

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        self.pp.setdefault(user_id, [])
        self.pp[user_id].append(post_id)
        pass

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        self.pr.setdefault(post_id, [])
        self.pr[post_id].append(user_id)
        pass

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        self.pf.setdefault(follower_user_id, [])
        self.pf[follower_user_id].append(followee_user_id)
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
        q = list()
        s = self.pf[user_id]
        for i in range(len(s)):
            for k1, v in self.pp.items():
                if s[i] == k1:
                    l1 = self.pp[s[i]]
                    for j in range(len(l1)):
                        q.append(l1[j])
        q = sorted(q, reverse=True)
        return q[:k]
        pass

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        kd = {}
        q = []
        ks = []
        for key in self.pr:
            self.pr[key] = list(set(self.pr[key]))
            s = len(self.pr[key])
            kd.setdefault(key, s)
            q.append(s)
        q = list(set(q))
        q = sorted(q, reverse=True)
        for i in range(len(q)):
            for k1, v in kd.items():
                if q[i] == v:
                    ks.append(k1)
        ks = ks[:k]
        return ks
        pass
