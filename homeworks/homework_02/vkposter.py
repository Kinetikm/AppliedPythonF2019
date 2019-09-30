#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.user_post = {}  # соотвествие пользователя и его постов
        self.view_post = {}  # соответсвие постов и пользователей посмотревших
        self.follow = {}  # соответсвие подписчика и "блогера"

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id in self.user_post.keys():
            self.user_post[user_id].append(post_id)
        else:
            self.user_post[user_id] = [post_id]

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if post_id in self.view_post.keys():
            if user_id not in self.view_post[post_id]:  # чтоб один и тот же 2 раза не смотрел
                self.view_post[post_id].append(user_id)
        else:
            self.view_post[post_id] = [user_id]

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id in self.follow.keys():
            if followee_user_id not in self.follow[follower_user_id]:  # чтоб 2 раза не подписывался
                self.follow[follower_user_id].append(followee_user_id)
        else:
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
        fresh_list = []
        if user_id in self.follow.keys():
            for followee in self.follow[user_id]:
                if followee in self.user_post.keys():
                    fresh_list.extend(self.user_post[followee])
        return sorted(fresh_list, reverse=True)[:k]

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        top_list = []
        new_view_post = {}  # соотвествие поста и количества его просмотров
        for i in self.view_post:
            new_view_post[i] = len(self.view_post[i])
        for post, see in sorted(new_view_post.items(), key=lambda i: (-i[1], -i[0])):
            top_list.append(post)
        if k <= len(top_list):
            top_list = top_list[0:k]
        return top_list
