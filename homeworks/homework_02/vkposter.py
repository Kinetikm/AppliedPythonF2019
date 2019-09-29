#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.all_posts = {}  # все посты post_id:list of user who read
        self.user_posts = {}  # user_id:list(post_id)
        self.user_subscriptions = {}  # user_id:user_subscriptions

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id. поста. Число.
        :return: ничего
        '''
        if user_id in self.user_posts:
            self.user_posts[user_id].append(post_id)
        else:
            self.user_posts[user_id] = [post_id]
        self.all_posts[post_id] = []

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if post_id in self.all_posts:
            if user_id not in self.all_posts[post_id]:
                self.all_posts[post_id].append(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id in self.user_subscriptions:
            self.user_subscriptions[follower_user_id].add(followee_user_id)
        else:
            s = set()
            s.add(followee_user_id)
            self.user_subscriptions[follower_user_id] = s

    def get_recent_posts(self, user_id: int, k: int)-> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        fpop_postsh_posts = []
        for itr in self.user_subscriptions[user_id]:
            if itr in self.user_posts:
                fpop_postsh_posts += self.user_posts[itr]
                fpop_postsh_posts.sort()
            if len(fpop_postsh_posts) > k:
                del fpop_postsh_posts[:len(fpop_postsh_posts) - k]
        fpop_postsh_posts = fpop_postsh_posts[::-1]
        return fpop_postsh_posts

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        pop_posts = []
        sorting = {}  # number of views:post id
        for t_post in self.all_posts:
            n = len(self.all_posts[t_post])
            if n not in sorting:
                sorting[n] = []
            sorting[n].append(t_post)
        t_list = sorted(sorting, reverse=True)
        for itr in t_list:
            sorting[itr].sort(reverse=True)# sort for posttime
            pop_posts += sorting[itr]
        if len(pop_posts) > k:
            pop_posts = pop_posts[:k]
        return pop_posts
