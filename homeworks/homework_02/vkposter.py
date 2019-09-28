#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.posts = {}  # посты пользователя
        self.follow = {}  # подписки пользователя
        self.posts_like = {}  # кол-во лайков у поста

    def user_posted_post(self, user_id, post_id):
        if user_id not in self.posts:
            self.posts[user_id] = []
        self.posts[user_id].append(post_id)

    def user_read_post(self, user_id, post_id):
        if post_id not in self.posts_like:
            self.posts_like[post_id] = []
        if user_id not in self.posts_like[post_id]:
            self.posts_like[post_id].append(user_id)

    def user_follow_for(self, follower_user_id, followee_user_id):
        if follower_user_id not in self.follow:
            self.follow[follower_user_id] = []
        self.follow[follower_user_id].append(followee_user_id)

    def get_recent_posts(self, user_id, k):
        mess = []
        for id in self.follow[user_id]:
            if id in self.posts:
                mess += self.posts[id][:-k - 1:-1]
        mess.sort()
        return mess[:-k - 1:-1]

    def get_most_popular_posts(self, k):
        mass = list(self.posts_like.items())
        mass.sort(key=lambda val: (len(val[1]), val[0]))
        mass = mass[:-k - 1:-1]
        return [x[0] for x in mass]
