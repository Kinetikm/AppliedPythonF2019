#!/usr/bin/env python
# coding: utf-8


class VKPoster:
    posts = {}
    # каждому посту сопоставляем список людей, его посмотревших
    users = {}
    # каждому пользователю сопоставляем список постов, просмотренных им
    follow = {}
    # зователю сопоставляем список его подписок
    fresh_posts = []
    # список из самых свежих постов
    rate_of_post = {}
    # количество просмотров каждого поста

    def __init__(self):
        raise NotImplementedError

    def user_posted_post(self, user_id: int, post_id: int):
        if not self.users[user_id]:
            self.users[user_id] = [post_id]
        else:
            self.users[user_id] += post_id
        self.posts[post_id] = [user_id]
        self.fresh_posts.insert(0, post_id)
        self.rate_of_post[post_id] = 1
        return


    def user_read_post(self, user_id: int, post_id: int):
        self.users[user_id] += post_id
        self.posts[post_id] += user_id
        self.rate_of_post[post_id] += 1

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if not self.follow[follower_user_id]:
            self.follow[follower_user_id] = []
        else:
            self.follow[follower_user_id] += followee_user_id

    def get_recent_posts(self, user_id: int, k: int) -> list:
        fresh_for_id = []
        for i in range(len(self.fresh_posts)):
            for folowee in self.follow[user_id]:
                if self.fresh_posts[i] in self.users[folowee]:
                    fresh_for_id += self.fresh_posts[i]
                    break
            if len(fresh_for_id) == k:
                return fresh_for_id

    def get_most_popular_posts(self, k: int) -> list:
        popular_posts = []
        count = len(self.rate_of_post)
        for post in self.fresh_posts:
            count = 0
            for other_post in self.rate_of_post.keys():
                if post > other_post:
                    count += 1
            if count > len(self.fresh_posts) - k:
                popular_posts += post
        return popular_posts
