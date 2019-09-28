#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.data_id = {}
        self.read_id = {}
        self.foll_id = {}

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self.data_id:
            self.data_id[user_id] = [post_id]
        else:
            self.data_id[user_id].append(post_id)
        return None

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if post_id not in self.read_id:
            self.read_id[post_id] = {user_id}
        else:
            self.read_id[post_id].add(user_id)
        return None

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id not in self.foll_id:
            self.foll_id[follower_user_id] = {follower_user_id}
        else:
            self.foll_id[follower_user_id].add(followee_user_id)
        return None

    def get_recent_posts(self, user_id: int, k: int)-> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        lupa = []
        for pupa in self.foll_id[user_id]:
            try:
                lupa += self.data_id[pupa]
            except KeyError:
                continue
        lupa = sorted(list(set(lupa)), reverse=True)
        return lupa[:k]

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        biba = []
        boba = []
        hiba = []
        hoba = {}
        for x in self.read_id:
            biba.append(len(self.read_id[x]))
            hoba[len(self.read_id[x])] = x
        biba = sorted(biba, reverse=True)[:k]
        for j in biba:
            hiba.append(hoba[j])
        hiba.sort(reverse=True)
        return hiba
