#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.posts = {}
        self.follows = {}

    def user_posted_post(self, user_id: int, post_id: int):
        if post_id not in self.posts:
            self.posts[post_id] = [user_id, []]

    def user_read_post(self, user_id: int, post_id: int):
        if post_id in self.posts:
            if user_id not in self.posts[post_id][1]:
                self.posts[post_id][1].append(user_id)
        else:
            self.posts[post_id] = [0, [user_id]]

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if follower_user_id in self.follows:
            if followee_user_id not in self.follows[follower_user_id]:
                self.follows[follower_user_id].append(followee_user_id)
        else:
            self.follows[follower_user_id] = [followee_user_id]

    def get_recent_posts(self, user_id: int, k: int) -> list:
        top = []
        if user_id in self.follows:
            post = sorted(self.posts.keys(), reverse=True)
            for i in post:
                if self.posts[i][0] in self.follows[user_id]:
                    if len(top) == k:
                        return top
                    top.append(i)
        return top

    def get_most_popular_posts(self, k: int) -> list:
        res = []
        posts = sorted(self.posts.items(), key=lambda post: len(post[1][1]), reverse=True)

        for i in range(len(posts)):
            for j in range(len(posts) - 1):
                if ((posts[j][0] < posts[j + 1][0]) and
                        (len(posts[j][1][1]) == len(posts[j + 1][1][1]))):
                    posts[j], posts[j + 1] = posts[j + 1], posts[j]

        for post in posts:
            if k == len(res):
                return res
            res.append(post[0])
        return res
