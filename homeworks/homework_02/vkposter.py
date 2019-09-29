#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.followed_for = {}
        self.read_by = {}
        self.posts = {}

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        self.posts[post_id] = user_id
        return None
        pass

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if post_id in self.read_by:
            self.read_by[post_id].add(user_id)
        else:
            self.read_by[post_id] = set()
            self.read_by[post_id].add(user_id)
        return None
        pass

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id in self.followed_for:
            self.followed_for[follower_user_id].append(followee_user_id)
        else:
            self.followed_for[follower_user_id] = []
            self.followed_for[follower_user_id].append(followee_user_id)
        return None
        pass

    def get_recent_posts(self, user_id: int, k: int)-> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        recent = []
        for key in sorted(self.posts, reverse=True):
            if self.posts[key] in self.followed_for[user_id] and len(recent) != k:
                recent.append(key)
            elif len(recent) == k:
                return recent
        return recent
        pass

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        new_dict = {key: len(value) for key, value in self.read_by.items()}
        unique = sorted(new_dict.values())
        unique.reverse()
        popular = []
        for i in unique[:k]:
            for key in sorted(new_dict.keys(), reverse=True):
                if new_dict[key] == i:
                    popular.append(key)
                    new_dict.pop(key)
                    break
        return popular
        pass
