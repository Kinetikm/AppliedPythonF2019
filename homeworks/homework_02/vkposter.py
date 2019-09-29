#!/usr/bin/env python
# coding: utf-8


class VKPoster:
    def __init__(self):
        self.lenta_of_user = dict()
        self.views_of_post = dict()
        self.folowers_of_user = dict()
        self.users_post = dict()

    def create_new_user(self, user_id):
        self.lenta_of_user[user_id] = set()
        self.folowers_of_user[user_id] = set()
        self.users_post[user_id] = set()

    def user_posted_post(self, user_id: int, post_id: int):
        if user_id not in self.lenta_of_user:
            self.create_new_user(user_id)
        self.views_of_post[post_id] = set()
        self.users_post[user_id].add(post_id)
        for whom in self.folowers_of_user[user_id]:
            self.lenta_of_user[whom].add(post_id)

    def user_read_post(self, user_id: int, post_id: int):
        if post_id not in self.views_of_post:
            self.views_of_post[post_id] = set()
        self.views_of_post[post_id].add(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if followee_user_id not in self.lenta_of_user:
            self.create_new_user(followee_user_id)
        if follower_user_id not in self.lenta_of_user:
            self.create_new_user(follower_user_id)
        if followee_user_id not in self.folowers_of_user:
            self.folowers_of_user[followee_user_id] = set()
        self.folowers_of_user[followee_user_id].add(follower_user_id)
        self.lenta_of_user[follower_user_id].update(
                self.users_post[followee_user_id])

    def get_recent_posts(self, user_id: int, k: int):
        c = list()
        if user_id in self.lenta_of_user:
            for item in self.lenta_of_user[user_id]:
                c.append(item)
        return sorted(c, reverse=True)[:k]

    def get_most_popular_posts(self, k: int):
        c = list()
        for item in self.views_of_post:
            c.append((len(self.views_of_post[item]), item))
        c.sort(key=lambda x: (-x[0], -x[1]))
        return list(map(lambda x: x[1], c))[:k]
