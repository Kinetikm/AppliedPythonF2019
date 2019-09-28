#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.Fol_Dict = {}
        self.Post_Read = {}
        self.User_Post = {}

    def user_posted_post(self, user_id: int, post_id: int):
        if post_id not in self.Post_Read:
            self.Post_Read[post_id] = set()
            if user_id not in self.User_Post:
                self.User_Post[user_id] = {post_id}
            self.User_Post[user_id].add(post_id)

    def user_read_post(self, user_id: int, post_id: int):
        if post_id not in self.Post_Read:
            self.Post_Read[post_id] = set()
        if user_id not in self.Post_Read[post_id]:
            self.Post_Read[post_id].add(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if follower_user_id not in self.Fol_Dict:
            self.Fol_Dict[follower_user_id] = set()
        self.Fol_Dict[follower_user_id].add(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int) -> list:
        if user_id in self.Fol_Dict:
            nl = []
            for user in self.Fol_Dict[user_id]:
                if user in self.User_Post:
                    nl += list(self.User_Post[user])
            if k > len(sorted(nl, reverse=True)):
                return sorted(nl, reverse=True)
            return sorted(nl, reverse=True)[:k]

    def get_most_popular_posts(self, k: int) -> list:
        nl = []
        for post in self.Post_Read:
            nl.append(post)
        nl.sort(reverse=True)
        nl.sort(key=lambda x: len(self.Post_Read[x]), reverse=True)
        if k > len(nl):
            return nl
        return nl[:k]
