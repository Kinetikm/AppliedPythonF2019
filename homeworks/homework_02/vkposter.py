#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.posts_id = []
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
        if user_id not in self.users:
            self.users[user_id] = []
        self.posts_id.append(post_id)
        self.posts[post_id] = [user_id]
        self.posts_id.sort()

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self.users:
            self.users[user_id] = []
        if post_id not in self.posts:
            self.posts_id.append(post_id)
            self.posts[post_id] = [None]
            self.posts_id.sort()
        if user_id not in self.posts[post_id]:
            self.posts[post_id].append(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id not in self.users:
            self.users[follower_user_id] = []
        if followee_user_id not in self.users:
            self.users[followee_user_id] = []
        if followee_user_id not in self.users[follower_user_id]:
            self.users[follower_user_id].append(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int)-> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        news_list = []
        if user_id not in self.users:
            self.users[user_id] = []
            return news_list
        if k == 0:
            return news_list
        for i in self.posts_id[::-1]:
            if self.posts[i][0] in self.users[user_id] and user_id not in self.posts[i]:
                news_list.append(i)
            if len(news_list) == k:
                break
        return news_list

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        pop_of_lst = []
        for i in self.posts_id:
            pop_of_lst.append(len(self.posts[i]))
        if k <= 0:
            return []
        if k > len(pop_of_lst):
            return [x for y, x in sorted(zip(pop_of_lst, self.posts_id))][::-1]
        return [x for y, x in sorted(zip(pop_of_lst, self.posts_id))][len(pop_of_lst)-k::][::-1]
