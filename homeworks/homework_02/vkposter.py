#!/usr/bin/env python
# coding: utf-8

import heapq


class VKPoster:

    def __init__(self):
        self.dict_of_posts = {}
        self.dict_of_users = {}
        self.dict_of_followers = {}
        self.dict_of_readers = {}

    def user_posted_post(self, user_id: int, post_id: int):
        self.dict_of_users.setdefault(user_id, []).append(post_id)
        self.dict_of_posts[post_id] = []

    def user_read_post(self, user_id: int, post_id: int):
        if user_id not in self.dict_of_posts.setdefault(post_id, []):
            self.dict_of_posts[post_id].append(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
            self.dict_of_followers.setdefault(follower_user_id, []).append(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int)-> list:
        list = []
        for i in self.dict_of_followers.setdefault(user_id, []):
            list.extend(self.dict_of_users.setdefault(i, []))
        list.sort()
        list.reverse()
        list = list[:k:]
        return list

    def get_most_popular_posts(self, k: int) -> list:
        tmp_list = []
        for id, val in self.dict_of_posts.items():
            heapq.heappush(tmp_list, (len(val), id))
        list = [i[1] for i in heapq.nlargest(k, tmp_list)]
        return list