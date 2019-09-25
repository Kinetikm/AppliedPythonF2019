#!/usr/bin/env python
# coding: utf-8

class VKPoster:

    d_author = {}
    d_read = {}
    d_follow = {}

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self.d_author:
            self.d_author[user_id] = []
        self.d_author[user_id] += [post_id]

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if post_id not in self.d_read:
            self.d_read[post_id] = set()
        self.d_read[post_id].add(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id not in self.d_follow:
            self.d_follow[follower_user_id] = []
        self.d_follow[follower_user_id] += [followee_user_id]

    def get_recent_posts(self, user_id: int, k: int)-> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        list_posts = []
        for followee in self.d_follow[user_id]:
            if followee in self.d_author:
                list_posts += self.d_author[followee]
        list_posts.sort()
        list_posts.reverse()
        return list_posts[:k:]

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        list_popular = []
        for post in self.d_read:
            list_popular += [(post, len(self.d_read[post]))]
        list_popular.sort(key = lambda i: i[1], reverse = True)
        k_most_popular = [i[0] for i in list_popular]
        return k_most_popular[:k:]
'''
vk = VKPoster()
vk.user_posted_post(122, 1)
vk.user_follow_for(122, 500)
vk.user_posted_post(500, 2)
print(vk.get_recent_posts(122, 1))
vk.user_follow_for(122, 50)
vk.user_posted_post(50, 4)
print(vk.get_recent_posts(122, 1))
print(vk.get_recent_posts(122, 2))
vk.user_read_post(122, 1)
vk.user_read_post(122, 2)
vk.user_read_post(50, 1)
print(vk.get_most_popular_posts(3))
'''