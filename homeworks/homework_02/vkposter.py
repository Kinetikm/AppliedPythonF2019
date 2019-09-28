#!/usr/bin/env python
# coding: utf-8


class VKPoster:
    def __init__(self):
        self.users = {}
        self.posts = {}
        self.followers = {}
        self.readers = {}

    def user_posted_post(self, user_id: int, post_id: int):
        if user_id in self.users.keys():
            self.users[user_id].append(post_id)
        else:
            self.users[user_id] = [post_id]

    def user_read_post(self, user_id: int, post_id: int):
        if user_id not in self.readers:
            self.readers[user_id] = [post_id]
            self.posts[post_id] = (self.posts[post_id] + 1) if post_id in self.posts.keys() else 1
        elif post_id not in self.readers[user_id]:
            self.readers[user_id].append(post_id)
            self.posts[post_id] = (self.posts[post_id] + 1) if post_id in self.posts.keys() else 1

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if followee_user_id != follower_user_id:
            if follower_user_id in self.followers.keys():
                self.followers[follower_user_id].append(followee_user_id)
            else:
                self.followers[follower_user_id] = [followee_user_id]

    def get_recent_posts(self, user_id: int, k: int) -> list:
        recent = []
        for blogger in self.followers[user_id]:
            if blogger in self.users.keys():
                recent.extend(self.users[blogger])
        return sorted(recent, reverse=True)[:k]

    def get_most_popular_posts(self, k: int) -> list:
        pops = []
        for every_post in sorted(self.posts.items(), key=lambda para: (-para[1], -para[0])):
            pops.append(every_post[0])
        return pops[:k]
