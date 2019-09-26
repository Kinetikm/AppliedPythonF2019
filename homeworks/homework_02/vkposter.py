#!/usr/bin/env python
# coding: utf-8
from homeworks.homework_02.homework_02_vk_poster_help import follower_helper, post_helper
from itertools import groupby


class VKPoster:

    def __init__(self):
        self.dict_posts = {}
        self.dict_followers = {}

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        new_post = post_helper.Post(post_id, user_id)
        self.dict_posts[post_id] = new_post
        pass

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if post_id in self.dict_posts:
            post = self.dict_posts[post_id]
            if user_id not in post.list_reading_user_id:
                post.list_reading_user_id.append(user_id)
        else:
            new_post = post_helper.Post(post_id, None)
            new_post.list_reading_user_id.append(user_id)
            self.dict_posts[post_id] = new_post
        pass

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id in self.dict_followers:
            self.dict_followers[follower_user_id].list_followee_user_id.append(followee_user_id)
        else:
            new_follower = follower_helper.Follower(follower_user_id)
            new_follower.list_followee_user_id.append(followee_user_id)
            self.dict_followers[follower_user_id] = new_follower
        pass

    def get_recent_posts(self, user_id: int, k: int) -> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''

        user = self.dict_followers[user_id]
        list_followee_user_id = user.list_followee_user_id
        list_post_by_followees = []
        for post_index in self.dict_posts:
            if self.dict_posts[post_index].create_user_id in list_followee_user_id:
                list_post_by_followees.append(post_index)
        list_post_by_followees.sort(reverse=True)
        return list_post_by_followees[:k]

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        list_dict_value = list(self.dict_posts.items())
        list_dict_value.sort(key=lambda post: len(post[1].list_reading_user_id), reverse=True)
        posts_group_by_len = [list(group) for k, group in
                              groupby(list_dict_value, lambda tuple: len(tuple[1].list_reading_user_id))]
        for key, sub_list in enumerate(posts_group_by_len):
            sub_list.sort(key=lambda tuple: tuple[0], reverse=True)
        return [tuple[0] for sublist in posts_group_by_len for tuple in sublist][:k]
