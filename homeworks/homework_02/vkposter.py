#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.read_posts = []
        self.users = []
        self.lenta = []
        self.posts = []

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
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
        cnt = True
        for i in self.posts:
            if i['post_id'] == post_id and user_id not in i['read']:
                i['read'].append(user_id)
                cnt = False
        if cnt and post_id not in [i['post_id'] for i in self.posts]:
            self.posts.append({'host_id': None, 'post_id': post_id, 'read': [user_id]})
        return

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if {'user_id': follower_user_id, 'followers': []} not in self.users:
            self.users.append({'user_id': follower_user_id, 'followers': []})
        if {'user_id': followee_user_id, 'followers': []} not in self.users:
            self.users.append({'user_id': followee_user_id, 'followers': []})
        for i in self.users:
            if i['user_id'] == followee_user_id:
                i['followers'].append(follower_user_id)
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
        for host in self.users:
            if user_id in host['followers']:
                for post in self.posts:
                    if post['host_id'] == host['user_id']:
                        if len(mas) < k:
                            mas.append(post['post_id'])
                        else:
                            if post['post_id'] > mas[-1]:
                                mas[0] = post['post_id']
                        mas.sort()
        return mas[::-1]

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
                fresh_posts.append({'id': i['post_id'], 'read': i['read']})
                fresh_posts = sorted(fresh_posts, key=lambda s: (len(s['read']), s['id']))
            else:
                for it in range(len(fresh_posts)):
                    if {'id': i['post_id'], 'read': i['read']} not in fresh_posts and\
                            (len(i['read']) > len(fresh_posts[it]['read']) or
                             (len(i['read']) == len(fresh_posts[it]['read']) and i['post_id'] > fresh_posts[it]['id'])):
                        fresh_posts[it] = {'id': i['post_id'], 'read': i['read']}
                        fresh_posts = sorted(fresh_posts, key=lambda s: (len(s['read']), s['id']))
        return [a['id'] for a in fresh_posts[::-1]]
