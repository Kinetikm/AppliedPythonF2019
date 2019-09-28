#!/usr/bin/env python
# coding: utf-8


class VKPoster:
    posts = {}
    # каждому посту сопоставляем список людей, его посмотревших
    create_post = {}
    # каждому пользователю сопоставляем список постов, просмотренных им
    follow = {}
    # зователю сопоставляем список его подписок
    fresh_posts = []
    # список из самых свежих постов
    rate_of_post = {}
    # количество просмотров каждого поста

    def __init__(self):
        return

    def user_posted_post(self, user_id: int, post_id: int):
        if user_id not in self.create_post:
            self.create_post[user_id] = []
        # если по данному пользователю не числится создание поста - начинаем список его постов
        self.create_post[user_id] += [post_id]
        # добавляем элемент в список данному user_id
        self.posts[post_id] = [user_id]
        # для нового поста создаем список людей его посмотревших
        self.fresh_posts.insert(0, post_id)
        # пополняем список свежих постов спереди
        self.rate_of_post[post_id] = 1
        # рейтинг нового поста автоматически становится равен единице - пользователь, его посмотревший
        return

    def user_read_post(self, user_id: int, post_id: int):
        self.posts[post_id] += [user_id]
        # пополняем список посмотревших пользователей для post_id
        self.rate_of_post[post_id] += 1
        # рейтинг поста тем временем пополняется

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if follower_user_id not in self.follow:
            self.follow[follower_user_id] = []
        # если для данного пользователя не было списка людей, на него подписанных - создаем
        self.follow[follower_user_id] += [followee_user_id]
        # пополняем список людей, на которых подписан follower_id

    def get_recent_posts(self, user_id: int, k: int) -> list:
        fresh_for_id = []
        for post in self.fresh_posts:
            for folowee in self.follow[user_id]:
                if post in self.create_post[folowee]:
                    fresh_for_id += [post]
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
                popular_posts += [post]
        return popular_posts
