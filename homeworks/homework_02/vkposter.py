#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.user_posted_dict = {}
        self.user_follows_dict = {}
        self.user_read_dict = {}
        self.post_popularity_dict = {}
        self.posts = []

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        self.post_popularity_dict[post_id] = 0
        if self.user_posted_dict.get(user_id, None):
            self.user_posted_dict[user_id].append(post_id)
        else:
            self.user_posted_dict[user_id] = [post_id]
        self.posts.append(post_id)

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if post_id not in self.posts:
            self.posts.append(post_id)
            self.post_popularity_dict[post_id] = 0

        if self.user_read_dict.get(user_id, None):
            if post_id not in self.user_read_dict[user_id]:
                self.post_popularity_dict[post_id] += 1
            self.user_read_dict[user_id].add(post_id)
        else:
            self.user_read_dict[user_id] = {post_id}
            self.post_popularity_dict[post_id] += 1

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if self.user_follows_dict.get(follower_user_id, None):
            self.user_follows_dict[follower_user_id].append(followee_user_id)
        else:
            self.user_follows_dict[follower_user_id] = [followee_user_id]

    def get_recent_posts(self, user_id: int, k: int) -> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        mass_ret = []
        u_fol_list = self.user_follows_dict[user_id]
        for i in sorted(self.posts, reverse=True):
            for j in u_fol_list:
                if i in self.user_posted_dict.get(j, []):
                    mass_ret.append(i)
                    if len(mass_ret) == k:
                        return mass_ret
                    else:
                        continue
        return mass_ret

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        self.post_popularity_dict = dict(sorted(self.post_popularity_dict.items(),
                                                key=lambda x: (x[1], sorted(self.posts).index(x[0])),
                                                reverse=True))
        return list(self.post_popularity_dict.keys())[:k]
