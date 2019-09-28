#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.user_posts = {}
        self.user_follows = {}
        self.user_read = {}
        self.most_popular = {}
        raise NotImplementedError

    def user_posted_post(self, user_id: int, post_id: int):
        if user_id in self.user_posts:
            self.user_posts[user_id].append(post_id)
        else:
            self.user_posts[user_id] = [post_id]
        self.most_popular[post_id] = 0
        pass

    def user_read_post(self, user_id: int, post_id: int):
        if (user_id not in self.user_read) or (post_id not in self.user_read[user_id]):
            if user_id in self.user_read:
                self.user_read[user_id].append(post_id)
            else:
                self.user_read[user_id] = [post_id]
            if post_id not in self.most_popular:
                self.most_popular[post_id] = 1
            else:
                self.most_popular[post_id] += 1
            pass

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if (follower_user_id in self.user_follows) and (followee_user_id != follower_user_id):
            self.user_follows[follower_user_id].append(followee_user_id)
        else:
            self.user_follows[follower_user_id] = [followee_user_id]
        pass

    def get_recent_posts(self, user_id: int, k: int) -> list:
        spisok = []
        for i in self.user_follows[user_id]:
            if i in self.user_posts:
                spisok.append(self.user_posts[i])
        spisok.sort()
        spisok.reverse()
        return spisok[:k]

    def get_most_popular_posts(self, k: int) -> list:
        spis = []
        for i, v in self.most_popular:
            spis.append([v, i])
        spis.sort()
        spis.reverse()
        vozv = spis[0:k]
        c = []
        for i in vozv:
            c.append(i[1])
        return c
