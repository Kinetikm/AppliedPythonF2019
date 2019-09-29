#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.users = {}
        self.posts = {}
        self.followers = {}

    def user_posted_post(self, user_id: int, post_id: int):
        if user_id not in self.users:
            self.users[user_id] = [post_id]
        else:
            self.users[user_id].append(post_id)

    def user_read_post(self, user_id: int, post_id: int):
        if post_id not in self.posts:
            self.posts[post_id] = [user_id]
        for id in self.posts[post_id]:
            flag = not (user_id == id)
        if flag:
            self.posts[post_id].append(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if follower_user_id not in self.users:
            self.users[follower_user_id] = []
        if follower_user_id not in self.followers:
            self.followers[follower_user_id] = [followee_user_id]
        else:
            self.followers[follower_user_id].append(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int)-> list:
        news = []
        for id in self.followers[user_id]:
            if id in self.users:
                news += self.users[id]
        news.sort()
        news = news[::-1]
        news = news[:k]
        return news

    def get_most_popular_posts(self, k: int) -> list:
        news_tmp = {}
        for id in self.posts:
            news_tmp[id] = len(self.posts[id])
        hot_news = list(news_tmp.items())
        hot_news.sort(key=lambda x: x[0], reverse=True)  # сортировка по свжести
        hot_news.sort(key=lambda x: x[1], reverse=True)  # сортировка по горячести
        popular_news = []
        for i in range(len(hot_news)):
            popular_news.append(hot_news[i][0])
        return popular_news[:k]
