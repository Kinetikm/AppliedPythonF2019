#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.d_author = {}
        self.d_read = {}
        self.d_follow = {}

    def user_posted_post(self, user_id: int, post_id: int):
        if user_id not in self.d_author:
            self.d_author[user_id] = []
        self.d_author[user_id] += [post_id]

    def user_read_post(self, user_id: int, post_id: int):
        if post_id not in self.d_read:
            self.d_read[post_id] = set()
        self.d_read[post_id].add(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if follower_user_id not in self.d_follow:
            self.d_follow[follower_user_id] = []
        self.d_follow[follower_user_id] += [followee_user_id]

    def get_recent_posts(self, user_id: int, k: int)-> list:
        list_posts = []
        for followee in self.d_follow[user_id]:
            if followee in self.d_author:
                list_posts += self.d_author[followee]
        list_posts.sort()
        list_posts.reverse()
        return list_posts[:k:]

    def get_most_popular_posts(self, k: int, list_popular=None) -> list:
        list_popular = list_popular or []
        for post in self.d_read:
            list_popular += [(post, len(self.d_read[post]))]
        list_popular.sort(key=lambda i: i[0])
        list_popular.sort(key=lambda i: i[1])
        list_popular.reverse()
        k_most_popular = [i[0] for i in list_popular]
        return k_most_popular[:k:]
