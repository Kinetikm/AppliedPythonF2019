#!/usr/bin/env python
# coding: utf-8
import operator


class VKPoster:

    def __init__(self):
        self.userPosts = dict()
        self.readPost = dict()
        self.followers = dict()
        self.postPop = dict()

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id in self.userPosts:
            self.userPosts[user_id].append(post_id)
        else:
            self.userPosts[user_id] = [post_id]

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self.readPost or post_id not in self.readPost[user_id]:
            self.readPost[user_id] = [post_id]
            if post_id not in self.postPop:
                self.postPop[post_id] = 1
            else:
                self.postPop[post_id] += 1

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id != followee_user_id:
            if follower_user_id in self.followers:
                self.followers[follower_user_id].append(followee_user_id)
            else:
                self.followers[follower_user_id] = [followee_user_id]

    def get_recent_posts(self, user_id: int, k: int) -> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        popularPosts = list()
        for num in self.followers[user_id]:
            if num in self.userPosts:
                popularPosts.extend(self.userPosts[num])
        return sorted(popularPosts, reverse=True)[:k]

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        mostPop = sorted(self.postPop.items(), key=operator.itemgetter(1), reverse=True)
        popList = [x[0] for x in mostPop]
        for i in range(len(popList)):
            if self.postPop[popList[i]] == self.postPop[popList[i - 1]] and popList[i] > popList[i - 1]:
                popList[i], popList[i - 1] = popList[i - 1], popList[i]
        return popList[:k]
