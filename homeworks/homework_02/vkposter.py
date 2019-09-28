#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.read_posts = []
        self.users = []
        self.lenta = []
        self.posts = []
        raise NotImplementedError

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        self.users.append({'user_id': user_id, 'followers': []})
        self.posts.append({'host_id': user_id, 'post_id': post_id, 'read': []})
        return

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        for i in self.posts:
            if i['post_id'] == post_id:
                i['read'].append(user_id)
        return

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        for i in self.users:
            if i['user_id'] == followee_user_id:
                i['follower'].append(follower_user_id)
        return

    def get_recent_posts(self, user_id: int, k: int)-> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        mas = []
        for user in self.users:
            if user['user_id'] == user_id:
                for post in self.posts:
                    if post['host_id'] in user['followers']:
                        mas.append(post['post_id'])
                        post['read'].appen(user_id)
        return mas

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        fresh_posts = []
        for i in self.posts:
            if len(fresh_posts) < k:
                fresh_posts.append(i['post_id'])
            else:
                if i['post_id'] > fresh_posts[-1]:
                    fresh_posts[-1] = i['post_id']
            fresh_posts.sort()
        return fresh_posts
