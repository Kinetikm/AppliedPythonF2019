#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.user_posts = {}
        self.posts = {}
        self.follows = {}

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self.user_posts.keys():
            self.user_posts[user_id] = [post_id]
        else:
            self.user_posts[user_id].append(post_id)
        self.posts[post_id] = 0

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self.readed.keys():
            self.readed[user_id] = [post_id]
            if post_id not in self.posts.keys():
                self.posts[post_id] = 1
            else:
                self.posts[post_id] += 1
        if post_id not in self.readed[user_id]:
            self.readed[user_id].append(post_id)
            if post_id not in self.posts.keys():
                self.posts[post_id] = 1
            else:
                self.posts[post_id] += 1

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id not in self.follows.keys():
            self.follows[follower_user_id] = [followee_user_id]
        else:
            self.follows[follower_user_id].append(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int):
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        output = []
        if user_id in self.follows.keys():
            for followee in self.follows[user_id]:
                if followee in self.user_posts.keys():
                    output.extend(self.user_posts[followee])
        return sorted(output, reverse=True)[:k]

    def get_most_popular_posts(self, k: int):
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        top = []
        for post, watch in sorted(self.posts.items(), key=lambda count: count[1], reverse=True):
            top.append(post)
        if k <= len(top):
            top = top[0:k]
        return sorted(top)
