#!/usr/bin/env python
# coding: utf-8


# from homeworks.homework_02.heap import MaxHeap
# from homeworks.homework_02.fastmerger import FastSortedListMerger


class VKPoster:

    def __init__(self):
        self.post_author = {}  # словарь автор:перечень написанных постов
        self.post_reader = {}  # id поста : список пользователей которые прочитали
        self.user_follow = {}  # юзер : на кого он подписан
        self.all_made_posts = []  # все осты которые были опубликованы

    #     это для проверки, когда мы читаем несуществующий пост

    def user_posted_post(self, user_id: int, post_id: int):
        self.all_made_posts.append(post_id)
        if user_id in self.post_author:
            self.post_author[user_id].append(post_id)
        else:
            self.post_author[user_id] = [post_id]

    def user_read_post(self, user_id: int, post_id: int):
        # if post_id in self.post_reader:
        #     if user_id not in self.post_reader[post_id]:
        #         self.post_reader[post_id].append(user_id)
        # else:
        #     self.post_reader[post_id] = [user_id]
        # self.all_made_posts.append(post_id)

        if post_id in self.post_reader:
            if user_id not in self.post_reader[post_id]:
                self.post_reader[post_id].append(user_id)
        else:
            self.post_reader[post_id] = [user_id]

        if post_id not in self.all_made_posts:
            self.all_made_posts.append(post_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if follower_user_id in self.user_follow:
            self.user_follow[follower_user_id].append(followee_user_id)
        else:
            self.user_follow[follower_user_id] = [followee_user_id]

    def get_recent_posts(self, user_id: int, k: int) -> list:
        podpiski = self.user_follow[user_id]
        postu = []
        for i in podpiski:
            if i in self.post_author:
                postu += self.post_author[i]
        all_user_post = postu or []
        all_user_post.sort(reverse=True)
        return all_user_post[:k]

    def get_most_popular_posts(self, k: int) -> list:

        pop_post = {}
        for key, value in self.post_reader.items():
            if len(value) in pop_post:
                pop_post[len(value)].append(key)
                pop_post[len(value)] = sorted(pop_post[len(value)], reverse=True)
            else:
                pop_post[len(value)] = [key]
        # sorted_dict = sorted(pop_post.items(), key=lambda x: x[1], reverse=True)
        print(pop_post)
        x = []
        for i in sorted(pop_post.keys(), reverse=True):
            x.append((i, pop_post[i]))
        print(x)
        result = []
        for i in range(len(x)):
            if k - len(x[i][1]) >= 0:
                result += x[i][1]
            else:
                result += x[i][1][:(k - len(x[i][1]))]
            k = k - len(x[i][1])
            print(result)
        return result
