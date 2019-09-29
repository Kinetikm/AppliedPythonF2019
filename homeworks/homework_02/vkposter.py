#!/usr/bin/env python
# coding: utf-8
from typing import List, Any


class VKPoster:

    def __init__(self):
        self.users = {}
        self.posts = {}

    def user_posted_post(self, user_id: int, post_id: int):
        if user_id not in self.users.keys():
            self.users[user_id] = [set() for i in range(3)]  # [ user's posts, user follows for, user's reads]
        self.users[user_id][0].add(post_id)
        self.posts[post_id] = 0

    def user_read_post(self, user_id: int, post_id: int):
        if user_id not in self.users.keys():
            self.users[user_id] = [set() for i in range(3)]  # [ user's posts, user follows for, user's reads]
        if post_id not in self.posts.keys():
            self.posts[post_id] = 0
        if (post_id not in self.users[user_id][2]) and (post_id not in self.users[user_id][0]):
            self.users[user_id][2].add(post_id)
            self.posts[post_id] += 1

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if follower_user_id not in self.users.keys():
            self.users[follower_user_id] = [set() for i in range(3)]  # [ user's posts, user follows for, user's reads]
        if followee_user_id not in self.users.keys():
            self.users[followee_user_id] = [set() for i in range(3)]  # [ user's posts, user follows for, user's reads]
        if followee_user_id != follower_user_id:
            self.users[follower_user_id][1].add(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int) -> list:
        temp = []
        for followed_user in self.users[user_id][1]:
            for i in self.users[followed_user][0]:
                temp.append(i)
        if k > len(temp):
            k = len(temp)
        temp.sort()
        list = temp[::-1][:k]
        return list

    def get_most_popular_posts(self, k: int) -> list:
        list = []
        temp = sorted(self.posts.items(), key=lambda a: (a[1], a[0]), reverse=True)
        if k > len(temp):
            k = len(temp)
        for i in range(k):
            list.append(temp[i][0])
        return list
