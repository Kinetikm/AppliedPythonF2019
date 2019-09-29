#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.posts = dict()
        self.reads = dict()
        self.readers = dict()
        self.followers = dict()

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id in self.posts:
            self.posts[user_id].append(post_id)
        else:
            self.posts[user_id] = [post_id]

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if post_id in self.readers:
            if user_id not in self.readers[post_id]:
                self.reads[post_id] += 1
            self.readers[post_id].append(user_id)
        else:
            self.reads[post_id] = 1
            self.readers[post_id] = [user_id]   

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
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
        out_list = list()
        for th in self.followers[user_id]:
            if th in self.posts:
                out_list += self.posts[th]
                out_list.sort()
        out_list = out_list[::-1]
        return out_list[:k]

       
    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        use_list = list()
        out_list = list()
        for key, val in self.reads.items():
            use_list.append([val, key])
        use_list.sort(reverse=True)
        for i in use_list[:k]:
            out_list.append(i[1])
        return out_list

