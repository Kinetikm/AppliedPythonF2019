#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.posts = dict()
        self.users = dict()
        self.follow = dict()

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        self.posts[post_id] = []
        try:
            self.users[user_id].append(post_id)
        except KeyError:
            self.users[user_id] = [post_id]

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if post_id in (self.posts.keys()):
            if user_id in self.posts[post_id]:
                return None
            else:
                try:
                    self.posts[post_id].append(user_id)
                except KeyError:
                    self.posts[post_id] = [user_id]
        else:
            self.posts[post_id] = [user_id]

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        try:
            self.follow[follower_user_id].append(followee_user_id)
        except KeyError:
            self.follow[follower_user_id] = [followee_user_id]

    def get_recent_posts(self, user_id: int, k: int)-> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        sort_list = list()
        for i in self.follow[user_id]:
            if i in (self.users.keys()):
                for j in self.users[i]:
                    sort_list.append(j)
            else:
                continue
        if len(sort_list) != 0:
            sort_list.sort()
            sort_list.reverse()
            return sort_list[:k]
        else:
            return sort_list

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        ret_list = list()
        dict_posts = dict()
        for key, value in self.posts.items():
            try:
                dict_posts[len(value)].append(key)
            except KeyError:
                dict_posts[len(value)] = [key]
        list_items = list(dict_posts.items())
        list_items.sort()
        for i in list_items:
            i[1].sort()
        for i in range(len(list_items)):
            for j in range(len(list_items[i][1])):
                ret_list.append(list_items[i][1][j])
        ret_list.reverse()
        ret_list = ret_list[:k]
        return ret_list
