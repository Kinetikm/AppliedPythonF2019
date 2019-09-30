#!/usr/bin/env python
# coding: utf-8

from collections import Counter


class VKPoster:

    def __init__(self):
        self.posted_post = {}  # словарь постов разных юзеров
        self.read_post = {}  # словарь прочитанных постов разными юзерами
        self.follower = {}  # список подписок разных юзеров

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self.posted_post:
            self.posted_post[user_id] = [post_id]
        else:
            self.posted_post[user_id].append(post_id)  # самые старые запощенные посты -  в начале

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self.read_post:
            self.read_post[user_id] = [post_id]
        else:
            self.read_post[user_id].append(post_id)  # самые старые прочитанные посты -  в начале

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id not in self.follower:
            self.follower[follower_user_id] = [followee_user_id]
        else:
            self.follower[follower_user_id].append(followee_user_id)  # самые старые подписки -  в начале

    def get_recent_posts(self, user_id: int, k: int) -> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        answer = []
        n = self.follower[user_id]

        for followee_user_id in n:
            if followee_user_id in self.posted_post:
                for post_id in self.posted_post[followee_user_id][-k:]:
                    answer.append(post_id)

        return sorted(sorted(answer)[-k:], reverse=True)

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        A = []
        for x in self.read_post.values():
            for post_id in set(x):
                A.append(post_id)

        n = Counter(A).most_common(k)
        for i in range(1, len(n)):
            if (n[i - 1][1] == n[i][1]) and (n[i - 1][0] < n[i][0]):
                n[i - 1], n[i] = n[i], n[i - 1]

        answer = []
        for x in n:
            answer.append(x[0])

        return answer
