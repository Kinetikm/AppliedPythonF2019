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

    def user_read_post(self, user_id, post_id):
        if post_id not in self.post_views:
            self.post_views[post_id] = set()
        self.post_views[post_id].add(user_id)

    def user_follow_for(self, follower_user_id, followee_user_id):
        if follower_user_id not in self.follow:
            self.follow[follower_user_id] = set()
        self.follow[follower_user_id].add(followee_user_id)

    def get_recent_posts(self, user_id, k)-> list:
        list_a = list(self.follow[user_id])
        list_b = []
        for user in list_a:
            list_b += self.users[user]
        list_b.sort(reverse=True)
        if len(list_b) >= k:
            return list_b[:k]
        else:
            return list_b

    def get_most_popular_posts(self, k: int)-> list:
        t_dict = {}
        for key in self.post_views:
            t_dict[key] = len(self.post_views[key])
        t_list = list(t_dict.items())
        t_list.sort(key=lambda elem: elem[0], reverse=True)
        t_list.sort(key=lambda elem: elem[1], reverse=True)
        list_of_most_popular = []
        for i in range(len(t_list)):
            list_of_most_popular.append(t_list[i][0])
        return list_of_most_popular[:k]
