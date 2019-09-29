#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.posts = []
        self.users = {}

    def user_posted_post(self, user_id: int, post_id: int):
        self.posts.append({"post_id": post_id, "user_id": user_id, "readed": []})
        if user_id in self.users:
            self.users[user_id]["posts"].append(len(self.posts) - 1)
        else:
            self.users[user_id] = {"posts": [len(self.posts) - 1], "followed": [], "added": []}

    def user_read_post(self, user_id: int, post_id: int):
        for i in self.posts:
            if post_id == i["post_id"] and user_id not in i["readed"]:
                i["readed"].append(user_id)
                if user_id not in self.users:
                    self.users[user_id] = {"posts": [], "followed": [], "added": []}
                return
        self.posts.append({"post_id": post_id, "user_id": None, "readed": [user_id]})

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if followee_user_id not in self.users:
            self.users[followee_user_id] = {"posts": [], "followed": [], "added": []}

        if follower_user_id in self.users:
            self.users[follower_user_id]["followed"].append(followee_user_id)
        else:
            self.users[follower_user_id] = {"posts": [], "followed": [followee_user_id], "added": []}

    def get_recent_posts(self, user_id: int, k: int)-> list:
        res = []
        i, correct = 0, 0
        self.posts.sort(key=lambda i: i["post_id"], reverse=True)
        while correct < k and i < len(self.posts):
            if self.posts[i]["user_id"] in self.users[user_id]["followed"] and \
                    user_id not in self.posts[i]["readed"]:
                res.append(self.posts[i]["post_id"])
                correct += 1
            i += 1
        return res

    def get_most_popular_posts(self, k: int) -> list:
        last_popular = self.posts
        last_popular.sort(key=lambda i: (len(i["readed"]), i["post_id"]), reverse=True)
        return [i["post_id"] for i in last_popular[:k]]
