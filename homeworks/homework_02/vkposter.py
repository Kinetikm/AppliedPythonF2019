#!/usr/bin/env python
# coding: utf-8

import heapq


class VKPoster:

    def __init__(self):
        self.users = {}
        self.posts = {}
        self.followers = {}
        self.reader = {}

    def user_posted_post(self, user_id: int, post_id: int):
        if user_id in self.users.keys():
            self.users[user_id].append(post_id)
        else:
            self.users[user_id] = [post_id]

    def user_read_post(self, user_id: int, post_id: int):
        if user_id in self.reader.keys():
            if post_id not in self.reader[user_id]:
                self.reader[user_id].append(post_id)
                if post_id in self.posts.keys():
                    self.posts[post_id] += 1
                else:
                    self.posts[post_id] = 1
        else:
            self.reader[user_id] = [post_id]
            if post_id in self.posts.keys():
                self.posts[post_id] += 1
            else:
                self.posts[post_id] = 1

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if follower_user_id in self.followers.keys():
            self.followers[follower_user_id].append(followee_user_id)
        else:
            self.followers[follower_user_id] = [followee_user_id]

    def get_recent_posts(self, user_id: int, k: int)-> list:
        list = []
        for s in self.followers[user_id]:
            if s in self.users.keys():
                list.extend(self.users[s])
        list = sorted(list, reverse=True)
        for i in range(len(list) - k):
            list.pop()
        return list

    def get_most_popular_posts(self, k: int) -> list:
        tmp_list = []
        for key, val in self.posts.items():
            tmp_list.append((val, key))
        list = [data[1] for data in tmp_list]
        return sorted(list, reverse=True)
