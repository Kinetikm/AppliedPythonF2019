#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.users_and_posts = dict()  # словарь, где хранится в ключе-user_id а в значении-post_id, который он запостил
        self.reed_posts = dict()  # словарь, где хранится в ключе-post_id а в значении-user_id, который читал этот пост
        self.followers_dict = dict()  # словарь, где хранится в ключе-пользователь а в значении-на кого он пописан

    def user_posted_post(self, user_id: int, post_id: int):
        if user_id not in self.users_and_posts:
            self.users_and_posts[user_id] = set()
        self.users_and_posts[user_id].add(post_id)
        self.reed_posts[post_id] = set()

    def user_read_post(self, user_id: int, post_id: int):
        if post_id not in self.reed_posts:
            self.reed_posts[post_id] = set()
        self.reed_posts[post_id].add(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if follower_user_id not in self.followers_dict:
            self.followers_dict[follower_user_id] = set()
        self.followers_dict[follower_user_id].add(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int) -> list:
        mas = []
        for i in self.followers_dict[user_id]:  # проверяем по подпискам
            if i not in self.users_and_posts:  # если юзер на которого мы подписаны ничего не выкладывал, то пропускаем
                continue
            else:
                for j in self.users_and_posts[i]:  # иначе считаем количество постов
                    mas.append(j)
        mas.sort(reverse=True)
        if (len(mas) < k):  # вывод
            return mas
        return mas[:k]

    def get_most_popular_posts(self, k: int) -> list:
        popular_dict = dict()
        popular_set = set()
        mas = []
        for i in self.reed_posts:  # составляем словарь popular_dict где в ключе лежит популярность, в значении post_id
            lenght = len(self.reed_posts[i])  # количество просмотров
            popular_set.add(lenght)  # сет состоящий из количеств просмотров
            if lenght not in popular_dict:
                popular_dict[lenght] = list()
            popular_dict[lenght].append(i)
        popular_list = list(popular_set)
        popular_list.sort(reverse=True)
        for i in popular_list:
            popular_dict[i].sort(reverse=True)  # сортируем по каждому ключу, чтобы потом в значении словаря лежали
            mas += popular_dict[i]  # отсортированные post_id и конктенируем в соответствии с популярностью
        if (len(mas) < k):
            return mas
        return mas[:k]
