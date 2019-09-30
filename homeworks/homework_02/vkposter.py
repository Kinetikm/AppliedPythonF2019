#!/usr/bin/env python
# coding: utf-8

import heapq


class VKPoster:

    def __init__(self):
        self.post_viewes = {}
        self.all_posts = {}
        self.user_follows = {}
        self.read_by_dict = {}


    def user_posted_post(self, user_id: int, post_id: int):
        self.all_posts.setdefault(user_id, []).append(post_id)
        self.read_by_dict[post_id] = []


    def user_read_post(self, user_id: int, post_id: int):
        if user_id not in self.all_posts:
            self.all_posts[post_id].append(user_id)


    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        self.user_follows.setdefault(follower_user_id, []).append(followee_user_id)


    def get_recent_posts(self, user_id: int, k: int)-> list:
        list = []
        for i in self.user_follows:
            list.extend(self.user_follows[i])
        return list.sort()[:k:-1]


    def get_most_popular_posts(self, k: int) -> list:
        list = []
        for i, read in self.all_posts.items():
            heapq.heappush(list, (len(read), i))
        list = [j[1] for j in heapq.nlargest(k, list)]
        return list
