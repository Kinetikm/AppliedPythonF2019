#!/usr/bin/env python
# coding: utf-8


user_posts = {}
user_views = {}
user_follows = {}
sequence_of_user_posts = []
post_views = {}
recent_posts = []
lst = []


class VKPoster:

    def __init__(self):
        raise NotImplementedError

    def user_posted_post(self, user_id: int, post_id: int):

        try:
            sequence_of_user_posts.index(post_id)
        except ValueError:
            sequence_of_user_posts.append(post_id)
        '''
        sequence_of_user_posts --> последовательность добавленных постов(list)
        '''
        try:
            user_posts[user_id].add(post_id)
        except KeyError:
            user_posts[user_id] = {post_id}
        return
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''

    def user_read_post(self, user_id: int, post_id: int):
        if post_id not in post_views:
            post_views[post_id] = 1
        else:
            post_views[post_id] = post_views[post_id] + 1
        '''
        post --> число просмотров для постов
        '''
        try:
            user_views[user_id].add(post_id)
        except KeyError:
            user_views[user_id] = {post_id}
        return
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        try:
            if followee_user_id not in user_follows[follower_user_id] or follower_user_id != followee_user_id:
                user_follows[follower_user_id].add(followee_user_id)
        except KeyError:
            if follower_user_id != followee_user_id:
                user_follows[follower_user_id] = {followee_user_id}
        return
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''

    def get_recent_posts(self, user_id: int, k: int)-> list:
        for j in range(k):
            for i in user_follows[user_id]:
                if sequence_of_user_posts[::-1][j] in user_posts[i]:
                    if sequence_of_user_posts[::-1][j] in recent_posts:
                        continue
                    else:
                        recent_posts.append(sequence_of_user_posts[::-1][j])
        return recent_posts
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''

    def get_most_popular_posts(self, k: int) -> list:
        l = []
        lst = []
        if k > len(post_views):
            k = len(post_views)
        for x in range(k):
            l.append(list(post_views.items())[x][::-1])
        l.sort()
        l.reverse()
        for x in range(k):
            lst.append(l[x][1])
        return lst
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
