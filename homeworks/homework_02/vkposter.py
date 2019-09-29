#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.users_posts = dict()
        self.followers = dict()
        self.readed_posts = dict()

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id in self.users_posts:
            self.users_posts[user_id] += [post_id]
        else:
            self.users_posts[user_id] = [post_id]
        return None    

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if post_id in self.readed_posts:
            self.readed_posts[post_id].add(user_id)
        else:
            self.readed_posts[post_id] = {user_id}
        return None 

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id in self.followers:
            self.followers[follower_user_id] += [followee_user_id]
        else:
            self.followers[follower_user_id] = [followee_user_id]
        return None

    def get_recent_posts(self, user_id: int, k: int) -> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        lst_recent = list()
        for i in self.followers[user_id]:
            if i in self.users_posts:
                lst_recent += self.users_posts[i]
        lst_recent = sorted(lst_recent, reverse=True)
        return lst_recent[:k]

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        rev_dict = dict()
        lst_popular = list()
        for i in self.readed_posts:
            if len(self.readed_posts[i]) in rev_dict:
                rev_dict[len(self.readed_posts[i])] += [i]
            else:
                rev_dict[len(self.readed_posts[i])] = [i]
        for i in sorted(rev_dict.keys(), reverse=True):
            rev_dict[i] = sorted(rev_dict[i], reverse=True)
            lst_popular += rev_dict[i]
        return lst_popular[:k]
