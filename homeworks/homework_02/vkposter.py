#!/usr/bin/env python
# coding: utf-8

from operator import itemgetter


class VKPoster:

    def __init__(self):
        # user - словарь:key = id_user, value = массив из постов
        self.users = dict()
        # reader - словарь:key = id_post, value = массив из постов
        self.reader = dict()
        # follower - словарь:key = id_user, value = массив его подписок
        self.follower = dict()

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id in self.users:
            # если пользователь есть
            # то добавляем ему пост id в массив его просмотренных постов
            self.users[user_id].append(post_id)
        else:
            # если пользователя нет,
            # то добавялем его в словарь пользователей
            # и id просмотренного поста
            self.users[user_id] = [post_id]

    def user_read_post(self, user_id: int, post_id: int):
        print(user_id, "read", post_id)
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        # если такой id поста есть,
        # то когда пользователь читает пост,
        # то в словарь читателей постов надо добавить новый пост

        if post_id not in self.reader:
            self.reader[post_id] = set()
        self.reader[post_id].add(user_id)

        print(self.reader)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id not in self.follower:
            self.follower[follower_user_id] = []
            # если id подписчика и пользователя не совпадают
            # и такой пользователь есть, то добавялем в словарь подписчикrов
        if follower_user_id != followee_user_id:
            self.follower[follower_user_id].append(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int) -> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        all_posts = []
        if user_id in self.follower:
            # проход по подпискам
            for sub_id in self.follower[user_id]:
                if sub_id in self.users:
                    all_posts.extend(self.users[sub_id])

        all_posts = sorted(all_posts)
        all_posts = all_posts[::-1]
        return all_posts[:k]

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        # print("===================")
        # print(number_reader)
        number_reader = \
            [(id_post, len(self.reader[id_post])) for id_post in self.reader]
        number_reader = sorted(number_reader, key=lambda tup: (tup[0], tup[1]))
        # print("dsfgds",number_reader)
        number_reader = sorted(number_reader, key=itemgetter(1))
        number_reader = number_reader[::-1]
        # print("*", number_reader)
        number_reader = number_reader[:k]
        number_reader = list(map(itemgetter(0), number_reader))
        # print("**", number_reader)
        return number_reader
