#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.users = {}
        self.posts = {}
        self.subs = {}

    def user_posted_post(self, user_id: int, post_id: int):
        if user_id in self.users.keys():
            self.users[user_id].append(post_id)
        else:
            self.users[user_id] = [post_id]

    def user_read_post(self, user_id: int, post_id: int):
        if user_id in self.users.keys() and post_id in self.posts.keys():
            if user_id not in self.posts[post_id]:
                self.posts[post_id].append(user_id)
        elif user_id in self.users.keys():
            self.posts[post_id] = [user_id]

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if follower_user_id in self.subs.keys():
            self.subs[follower_user_id].append(followee_user_id)
        else:
            self.subs[follower_user_id] = [followee_user_id]

    def get_recent_posts(self, user_id: int, k: int)-> list:
        tmp = []
        if user_id in self.subs.keys():
            for i in range(len(self.subs[user_id])):
                self.users[i].sort()
                for j in range(k):
                    tmp.append(self.users[i][j])
        return tmp

    def get_most_popular_posts(self, k: int) -> list:
        tmp = []
        for key, value in enumerate(self.posts):
            tmp.append(key, len(value))
        tmp.sort(tmp, key=lambda tmp: tmp[1], reverse=True)
        tmp.sort(tmp, key=lambda tmp: tmp[0], reverse=True)
        res = []
        for i in range(k):
            res.append(tmp[i][0])
        return res
