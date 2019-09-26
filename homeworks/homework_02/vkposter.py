#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self._posts = {}
        self._nr = {}
        self._followers = {}
        self._news = {}

    def form_news(self, follower_user_id, followee_user_id, new):
        if follower_user_id not in self._news:
            self._news[follower_user_id] = []
        if not isinstance(new, list):
            new = [new]
        self._news[follower_user_id].extend(new)

    def user_posted_post(self, user_id: int, post_id: int):
        if user_id not in self._posts:
            self._posts[user_id] = []
        self._posts[user_id].append(post_id)
        if user_id in self._followers:
            for i in self._followers[user_id]:
                self.form_news(i, user_id, post_id)

    def user_read_post(self, user_id: int, post_id: int):
        if post_id not in self._nr:
            self._nr[post_id] = set()
        self._nr[post_id].add(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if followee_user_id not in self._followers:
            self._followers[followee_user_id] = []
        self._followers[followee_user_id].append(follower_user_id)
        x = followee_user_id
        if followee_user_id in self._posts:
            self.form_news(follower_user_id, followee_user_id, self._posts[x])

    def get_recent_posts(self, user_id: int, k: int)-> list:
        if user_id in self._news:
            result = sorted(self._news[user_id])
            if k >= len(result):
                return result[len(result) - 1::-1]
            return result[len(result) - 1:len(result) - k - 1: -1]
        return []

    def get_most_popular_posts(self, k: int) -> list:
        res = sorted(self._nr.items(), key=lambda x: (len(x[1]), x[0]))
        res = list(map(lambda x: x[0], res))
        if k >= len(res):
            return res[len(result) - 1::-1]
        return res[len(res) - 1:len(res) - k - 1: -1]
