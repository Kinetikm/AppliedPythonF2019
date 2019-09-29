#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.users = dict()
        self.posts = dict()

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self.users:
            self.users[user_id] = [[], [], [], []]  # посты, подписки(на кого),подписчики, лента
        self.users[user_id][0].append(post_id)
        if post_id not in self.posts:
            self.posts[post_id] = set()
        for followers in self.users[user_id][2]:
            self.users[followers][3].append(post_id)

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self.users:
            self.users[user_id] = [[], [], [], []]  # посты, подписки(на кого),подписчики, лента
        if post_id not in self.posts:
            self.posts[post_id] = set()
        self.posts[post_id].add(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id not in self.users:
            self.users[follower_user_id] = [[], [], [], []]  # посты, подписки(на кого),подписчики, лента
        if followee_user_id not in self.users:
            self.users[followee_user_id] = [[], [], [], []]  # посты, подписки(на кого),подписчики, лента
        self.users[follower_user_id][1].append(followee_user_id)
        self.users[followee_user_id][2].append(follower_user_id)
        self.users[follower_user_id][3] += self.users[followee_user_id][0]

    def get_recent_posts(self, user_id: int, k: int) -> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        self.users[user_id][3].sort(reverse=1)
        if k >= len(self.users[user_id][3]):
            return self.users[user_id][3]
        return self.users[user_id][3][0:k]

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        list_of_posts = list(self.posts.items())
        # сортировка по популярности
        list_of_posts.sort(key=lambda x: len(x[1]))
        n = 0
        # сортировка по свежести
        for i in range(1, len(list_of_posts)):
            if len(list_of_posts[i][1]) > len(list_of_posts[i - 1][1]):
                temp = list_of_posts[n:i]
                temp.sort(key=lambda x: x[0])
                list_of_posts[n:i] = temp
                n = i
        temp = list_of_posts[n::]
        temp.sort(key=lambda x: x[0])
        list_of_posts[n::] = temp
        # сборка в финальный массив(на вывод)
        final = []
        for i in list_of_posts:
            final.append(i[0])
        final = final[::-1]
        if k >= len(final):
            return final
        return final[0:k]
