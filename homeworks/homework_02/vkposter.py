#!/usr/bin/env python
# coding: utf-8


class VKPoster:
    def __init__(self):
        self.post = {}  # ключ - post_id, значение-list_user_id
        self.read = {}  # ключ - post_id, значение-set_user_id
        self.follow = {}  # ключ - follow_id, значение-list_followee_id

    def user_posted_post(self, user_id: int, post_id: int):
        if post_id not in self.post:
            self.post[post_id] = []
        self.post[post_id] = user_id

    def user_read_post(self, user_id: int, post_id: int):
        if post_id not in self.read:
            self.read[post_id] = set()
        self.read[post_id].add(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if follower_user_id not in self.follow:
            self.follow[follower_user_id] = []
        self.follow[follower_user_id] += [followee_user_id]

    def get_recent_posts(self, user_id: int, k: int) -> list:
        ich_new_post = sorted(self.post.keys(), reverse=True)
        ich_new_post_id = []
        for post in ich_new_post:
            if self.post[post] in self.follow[user_id]:
                ich_new_post_id += [post]
            if len(ich_new_post_id) == k:
                return ich_new_post_id
        return ich_new_post_id

    def get_most_popular_posts(self, k: int) -> list:
        ich_dict = {}
        for key in self.read:
            ich_dict[key] = len(self.read[key])
        ich_list = list(ich_dict.items())
        ich_list.sort(key=lambda i: i[0], reverse=True)
        ich_list.sort(key=lambda i: i[1], reverse=True)
        ich_famous = []
        for i in range(len(ich_list)):
            if len(ich_famous) == k:
                return ich_famous
            ich_famous.append(ich_list[i][0])
        ich_famous.sort(reverse=True)
        return ich_famous
