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
        fresh_posts = []
        for itr in self.user_subscriptions[user_id]:
            if itr in self.user_posts:
                fresh_posts += self.user_posts[itr]
                fresh_posts.sort()
            if len(fresh_posts) > k:
                del fresh_posts[:len(fresh_posts) - k]
        fresh_posts = fresh_posts[::-1]
        return fresh_posts

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        sorting_list = []
        pop_posts = []
        for itr in self.all_posts:
            sorting_list.append((len(self.all_posts[itr]), itr))
        sorting_list.sort(reverse=True)
        for i in range(k):
            pop_posts.append(sorting_list[i][1])
        return pop_posts
