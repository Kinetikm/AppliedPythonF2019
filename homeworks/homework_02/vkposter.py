#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.users = {}
        # Ключи - айдишники пользователей.
        # Элементы - списки из их подписчиков.
        self.posts = {}
        # Ключи - айдишники постов
        # Элементы - списки из айдишников просмотревших (создатель первый).

    def user_posted_post(self, user_id: int, post_id: int):
        if user_id not in self.users.keys():
            self.users.update({user_id: []})
        self.posts.update({post_id: [user_id]})
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''

    def user_read_post(self, user_id: int, post_id: int):
        if self.posts.get(post_id) is None:
            self.posts.update({post_id: ['unknown_author']})
        if user_id not in self.posts[post_id]:
            self.posts[post_id].append(user_id)
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if self.users.get(follower_user_id) is None:
            self.users.update({follower_user_id: []})
        if self.users.get(followee_user_id) is None:
            self.users.update({followee_user_id: []})
        self.users[follower_user_id].append(followee_user_id)
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''

    def get_recent_posts(self, user_id: int, k: int) -> list:
        Res = []
        for post_id in self.posts.keys():
            if self.posts[post_id][0] in self.users[user_id]:
                if user_id not in self.posts[post_id]:
                    Res.append(post_id)
        Res = sorted(Res, key=lambda post_id: -post_id)
        if k < len(Res):
            return Res[:k]
        return Res
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''

    def get_most_popular_posts(self, k: int) -> list:
        Res = []
        for post_id in self.posts.keys():
            Res.append((len(self.posts[post_id])-1, post_id))
        Res = sorted(Res, key=lambda tup: (-tup[0], -tup[1]))
        Res = Res[:min(k, len(Res))]
        return [tup[1] for tup in Res]
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
