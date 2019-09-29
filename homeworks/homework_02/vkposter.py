#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.dict_user_id = {}
        self.dict_post_id = {}

    def user_posted_post(self, user_id: int, post_id: int):
        if not self.dict_user_id.get(user_id):
            self.dict_user_id[user_id] = []
        self.dict_post_id[post_id] = [user_id]

    def user_read_post(self, user_id: int, post_id: int):
        if not self.dict_post_id.get(post_id):
            self.dict_post_id[post_id] = ['creator_id']
        if user_id not in self.dict_post_id[post_id]:
            self.dict_post_id[post_id].append(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if not self.dict_user_id.get(follower_user_id):
            self.dict_user_id[follower_user_id] = []
        self.dict_user_id[follower_user_id].append(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int)-> list:
        lst = []
        for i in self.dict_post_id.keys():
            if self.dict_post_id[i][0] in self.dict_user_id[user_id]:
                lst.append(i)
        lst.sort(reverse=True)
        return lst[:min(k, len(lst))]

    def get_most_popular_posts(self, k: int) -> list:
        lst = []
        for i in self.dict_post_id.keys():
            lst.append((len(self.dict_post_id[i]), i))
        lst = sorted(lst, key=lambda f: (f[0], f[1]), reverse=True)
        lst = [lst[i][1] for i in range(min(k, len(lst)))]
        return lst
