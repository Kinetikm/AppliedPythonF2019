#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.UsersPosts = {}
        self.PostsReaders = {}
        self.UsersFollowees = {}

    def user_posted_post(self, user_id: int, post_id: int):
        validation = True
        for k in self.UsersPosts.keys():
            if post_id in self.UsersPosts[k]:
                validation = False
        if validation is True:
            if user_id in self.UsersPosts:
                self.UsersPosts[user_id].append(post_id)
            else:
                self.UsersPosts[user_id] = [post_id]
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''

    def user_read_post(self, user_id: int, post_id: int):
        if post_id not in self.PostsReaders.keys():
            self.PostsReaders[post_id] = [user_id]
        elif user_id not in self.PostsReaders[post_id]:
            self.PostsReaders[post_id].append(user_id)
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if follower_user_id != followee_user_id:
            if follower_user_id not in self.UsersFollowees:
                self.UsersFollowees[follower_user_id] = [followee_user_id]
            elif followee_user_id not in self.UsersFollowees[follower_user_id]:
                self.UsersFollowees[follower_user_id].extend([followee_user_id])
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''

    def get_recent_posts(self, user_id: int, k: int)-> list:
        feed = []
        for followee in self.UsersFollowees[user_id]:
            if followee in self.UsersPosts.keys():
                feed.extend(self.UsersPosts[followee])
        return sorted(feed, reverse=True)[:k]
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''

    def get_most_popular_posts(self, k: int) -> list:
        popularfeed = []
        for post in self.PostsReaders:
            popularfeed.append((post, len(self.PostsReaders[post])))
        popularfeed.sort(key=lambda i: i[1], reverse=True)
        for i in range(len(popularfeed)-1):  # why not))
            for j in range(len(popularfeed)-1-i):
                if popularfeed[j][1] == popularfeed[j+1][1]:
                    if popularfeed[j][0] < popularfeed[j+1][0]:  # Более свежий вперед
                        popularfeed[j], popularfeed[j+1] = popularfeed[j+1], popularfeed[j]
        for i in range(len(popularfeed)):  # перезапись
            popularfeed[i] = popularfeed[i][0]
        return popularfeed[:k]
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
