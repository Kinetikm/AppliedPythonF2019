#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.users = {}
        self.posts = {}
        self.subs = {}
    def user_posted_post(self, user_id: int, post_id: int):
        if user_id in self.users.keys():
            self.users[user_id].append(post_id)
        else:
            self.users.update({user_id: [post_id]})

    def user_read_post(self, user_id: int, post_id: int):
        if user_id in self.users.keys() and post_id in self.posts.keys():
            self.posts[post_id].append(user_id)
        elif user_id in self.users.keys():
            self.posts.update({post_id: [user_id]})

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if follower_user_id in self.subs.keys():
            self.subs[follower_user_id].append(followee_user_id)
        else:
            self.subs.update({follower_user_id: [followee_user_id]})


    def get_recent_posts(self, user_id: int, k: int)-> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        tmp = ()
        if user_id in self.subs.keys():
            for i in range(len(self.subs[user_id])):
                sorted(self.users[i])
                for j in range(k):
                    tmp.append(self.users[i][j])
        return tmp


    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        tmp = ()
        for key,value in enumerate(self.posts):
            tmp.append(key, len(value))
        sorted(tmp, key = lambda tmp: tmp[1])
        sorted(tmp, key = lambda tmp: tmp[0], reverse = True)
        res = ()
        for i in range(k):
            res.append(tmp[i][0])
        tmp = ()
        return res


