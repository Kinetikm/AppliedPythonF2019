#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.users = {}
        self.follow = {}
        self.post_views = {}

    def user_posted_post(self, user_id: int, post_id: int):
        if user_id not in self.users:
            self.users[user_id] = []
        self.users[user_id].append(post_id)

    def user_read_post(self, user_id: int, post_id: int):
        if post_id not in self.post_views:
            self.post_views[post_id] = set()
        self.post_views[post_id].add(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if follower_user_id not in self.follow:
            self.follow[follower_user_id] = set()
        self.follow[follower_user_id].add(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int)-> list:
        a = list(self.follow[user_id])  # список юзеров, на которых подписан user_id
        b = []  # список постов, тех на кого подписан user_id
        for user in a:
            b += self.users[user]
        b.sort(reverse=True)
        if len(b) >= k:
            return b[:k]
        else:
            return b

    def get_most_popular_posts(self, k: int) -> list:
        tmp_dict = {}                   # временный словарь, хранящий ключём post_id, а значением длину множества юзеров
        for key in self.post_views:
            tmp_dict[key] = len(self.post_views[key])
        tmp_list = list(tmp_dict.items())   # временный список кортежей, для сортировки
        tmp_list.sort(key=lambda elem: elem[0], reverse=True)
        tmp_list.sort(key=lambda elem: elem[1], reverse=True)
        list_of_most_popular = []       # список с отсортированными post_id
        for i in range(len(tmp_list)):
            list_of_most_popular.append(tmp_list[i][0])
        list_of_most_popular = list_of_most_popular[:k]
        list_of_most_popular.sort(reverse=True)
        return list_of_most_popular
