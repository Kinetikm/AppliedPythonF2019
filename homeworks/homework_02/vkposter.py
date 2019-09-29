#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.posts = {}
        # каждому посту сопоставляем список людей, его посмотревших
        self.follow = {}
        # каждому пользователю сопоставляем список его подписок
        self.post_stats = {}
        # статистика чтения поста

    def user_posted_post(self, user_id: int, post_id: int):
        self.posts[post_id] = user_id
        # каждому посту сопоставляем его создателя

    def user_read_post(self, user_id: int, post_id: int):
        if post_id not in self.post_stats:
            self.post_stats[post_id] = set()
        # если у поста еще нет пользователей, его посмотревших, то создаем новую коллекцию
        self.post_stats[post_id].add(user_id)
        # добавляем в соответствующую посту коллекцию нового посмотревшего пост человека

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if follower_user_id not in self.follow:
            self.follow[follower_user_id] = []
        # если для данного пользователя не было списка людей, на него подписанных - создаем
        self.follow[follower_user_id] += [followee_user_id]
        # пополняем список людей, на которых подписан follower_id

    def get_recent_posts(self, user_id: int, k: int) -> list:
        fresh_posts = sorted(self.posts.keys())
        fresh_posts.reverse()
        fresh_for_id = []
        for post in fresh_posts:
            if self.posts[post] in self.follow[user_id]:
                fresh_for_id += [post]
            if len(fresh_for_id) == k:
                return fresh_for_id
        return fresh_for_id

    def get_most_popular_posts(self, k: int) -> list:
        new_dict = {key: len(value) for key, value in self.post_stats.items()}
        most_popular = sorted(new_dict.values())
        most_popular.reverse()
        popular_posts = []
        for value in most_popular[:k]:
            for key in sorted(new_dict.keys(), reverse=True):
                if new_dict[key] == value:
                    popular_posts.append(key)
                    new_dict.pop(key)
                    break
        return popular_posts
