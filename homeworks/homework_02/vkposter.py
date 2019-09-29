#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.users_and_posts = {}
        self.posts_are_read_by = {}
        self.rate = {}
        self.followees = {}

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id in self.users_and_posts:
            self.users_and_posts[user_id] += [post_id]
        else:
            self.users_and_posts[user_id] = [post_id]

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if post_id in self.posts_are_read_by:
            if user_id not in self.posts_are_read_by[post_id]:
                self.posts_are_read_by[post_id] += [user_id]
                self.rate[post_id] += 1
        else:
            self.rate[post_id] = 1
            self.posts_are_read_by[post_id] = [user_id]

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id in self.followees:
            self.followees[follower_user_id].add(followee_user_id)
        else:
            self.followees[follower_user_id] = {followee_user_id}

    def get_recent_posts(self, user_id: int, k: int) -> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        all_latest_k_posts = []
        for followee in self.followees[user_id]:
            if followee in self.users_and_posts:
                if len(self.users_and_posts[followee]) > k:
                    self.users_and_posts[followee].sort(reverse=True)
                    all_latest_k_posts += self.users_and_posts[followee][0:k]
                else:
                    all_latest_k_posts += self.users_and_posts[followee]
            all_latest_k_posts.sort(reverse=True)
        return all_latest_k_posts[0:k]

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        leaders = sorted(self.rate.values(), reverse=True)
        pop_posts = []
        pop_lead = []
        i = 0
        len_res = 0
        while i != k:
            for post, rating in self.rate.items():
                if rating == leaders[i]:
                    pop_posts += [post]
                    len_res += 1
            pop_posts.sort(reverse=True)
            pop_lead += pop_posts
            pop_posts = []
            if len_res >= k:
                i = k
            else:
                i += 1
        return pop_lead[0:k]
