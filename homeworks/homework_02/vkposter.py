#!/usr/bin/env python
# coding: utf-8


def cache_user(f):
    cache = set()

    def ret_f(self, user_id, post_id):
        if (user_id, post_id) in cache:
            return
        f(self, user_id, post_id)
        cache.add((user_id, post_id))
    return ret_f


class VKPoster:
    def __init__(self):
        self.data = []
        self.follow_user = dict()
        self.set_post_id = set()

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        self.data.append([post_id, user_id, 0])
        self.set_post_id.add(post_id)

    @cache_user
    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if post_id not in self.set_post_id:
            self.user_posted_post(user_id, post_id)
        for it in self.data:
            if it[0] == post_id:
                it[2] += 1
                break

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id not in self.follow_user:
            self.follow_user[follower_user_id] = []
        self.follow_user[follower_user_id].append(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int)-> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        k = min(k, len(self.data))
        res = []
        for it in self.data:
            if it[1] in self.follow_user[user_id]:
                res.append(it[0])
        res.sort(reverse=True)
        return res[0:k]

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        k = min(k, len(self.data))
        res = sorted(self.data, key=lambda x: x[0], reverse=True)
        res.sort(key=lambda x: x[2], reverse=True)
        res = [it[0] for it in res[0:k]]
        return res
