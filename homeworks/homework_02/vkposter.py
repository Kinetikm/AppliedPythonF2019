#!/usr/bin/env python
# coding: utf-8


from homeworks.homework_02.heap import MaxHeap
from homeworks.homework_02.fastmerger import FastSortedListMerger


class VKPoster:

    def __init__(self):
        self.users = {}
        self.posts = {}
        self.followers = {}

    def user_posted_post(self, user_id: int, post_id: int):
        if user_id not in self.posts:
            self.posts[user_id] = [post_id]
        else:
            self.posts[user_id].append(post_id)

    def user_read_post(self, user_id: int, post_id: int):
        if post_id not in self.posts:
            self.posts[post_id] = [user_id]
        for id in posts[post_id]:
            flag = not (user_id == id)
        if flag:
            self.posts[post_id].append(user_id)


    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if folower_user_id not in self.users:
            self.users[folower_user_id] = []
        if folower_user_id not in self.followers:
            self.followers[follower_user_id] = [followee_user_id]
        else:
            self.followers[follower_user_id].append(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int)-> list:
        news = []
        for id in self.follow[user_id]:
           if id in self.users():
                news += self.users[id]
        news.sort()
        news = news[::-k]
        news = news[:k:]
        return news

    def get_most_popular_posts(self, k: int) -> list:
        news_tmp = {}
        for id in self.news_tmp:
            news_tmp[key] = len(self.post_views[key])
        hot_news = list(news_tmp.items())
        hot_news.sort(key=lambda elem: elem[0], reverse=True) #сортировка по свжести
        hot_news.sort(key=lambda elem: elem[1], reverse=True) #сортировка по горячести
        popular_news = []
        for i in range(len(hot_news)):
            popular_news.append(hot_news[i][0])
        return popular_news[:k]
