# !/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.users = {}
        self.posts = {}
        # raise NotImplementedError

    def user_posted_post(self, user_id: int, post_id: int):
        self.user_sign(user_id)
        self.users[user_id]['posts'] += [post_id]
        pass

    def user_read_post(self, user_id: int, post_id: int):
        self.user_sign(user_id)
        self.users[user_id]['views'] += [post_id]
        pass

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        self.user_sign(follower_user_id)
        self.users[follower_user_id]['follows'] += [followee_user_id]
        pass

    def get_recent_posts(self, user_id: int, k: int) -> list:
        self.user_sign(user_id)
        newest_posts = [0]
        for i in self.users[user_id]['follows']:
            for j in self.users[i]['posts']:
                for jj in range(len(newest_posts)):
                    if j > newest_posts[jj]:
                        newest_posts.insert(jj, j)
                        newest_posts = newest_posts[:k]
                        break
        return newest_posts
        pass

    def get_most_popular_posts(self, k: int) -> list:
        post_lst = [0]
        for i in self.users:
            for j in self.users[i]['views']:
                self.post_pop(j)
        for i in self.posts:
            for j in range(len(post_lst)):
                if self.posts[i] > post_lst[j]:
                    post_lst.insert(j, i)
                    post_lst = post_lst[:k]
        post_lst.sort(reverse=True)
        return post_lst
        pass

    def user_sign(self, user_id):
        if self.users.get(user_id) is None:
            self.users[user_id] = {'posts': [], 'views': [], 'follows': []}
        return None

    def post_pop(self, post_id):
        if self.posts.get(post_id) is None:
            self.posts[post_id] = 1
        else:
            self.posts[post_id] += 1
        return None
