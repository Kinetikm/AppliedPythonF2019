#!/usr/bin/env python
# coding: utf-8


#from homeworks.homework_02.heap import MaxHeap
#from homeworks.homework_02.fastmerger import FastSortedListMerger

class VKPoster:

    #users = dict()  # key = user_id; value = User

    def __init__(self):
        self.users = dict()
        self.users[1.1] = User(1.1)

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self.users.keys():
            self.users[user_id] = User(user_id)
        self.users[user_id].new_post(post_id)
        # for user in list(self.users.values()):
        #     print(user.posts)
        print("vk.user_posted_post(", user_id, ",", post_id, ")")

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self.users.keys():
            self.users[user_id] = User(user_id)
        mas = []
        for user in self.users.values():
            for ii in user.posts:
                mas.append(ii)
        if post_id not in mas:
            self.users[1.1].new_post(post_id)
        self.users[user_id].new_read(post_id)
        # for user in list(self.users.values()):
        #     print(user.posts)
        print('vk.user_read_post(', user_id, ",", post_id, ")")

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id not in self.users.keys():
            self.users[follower_user_id] = User(follower_user_id)
        if followee_user_id not in self.users.keys():
            self.users[followee_user_id] = User(followee_user_id)
        if follower_user_id != followee_user_id:
            self.users[follower_user_id].new_subscribe(followee_user_id)
        # for user in list(self.users.values()):
        #     print(user.posts)
        print('vk.user_follow_for(', follower_user_id, ",", followee_user_id, ")")

    def get_recent_posts(self, user_id: int, k: int)-> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        if user_id not in self.users.keys():
            self.users[user_id] = User(user_id)
        new_posts = []
        for user in self.users[user_id].subscribes:
            for post_id in self.users[user].posts:
                if post_id not in new_posts:
                    new_posts.append(post_id)
        new_posts.sort(reverse=True)
        # for user in list(self.users.values()):
        #     print(user.posts)
        print('vk.get_recent_posts(', user_id, ",", k, ")")
        return new_posts[0:k:]

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        print('vk.get_most_popular_posts(', k, ')')
        mas = []
        print(self.users.keys())
        for user in list(self.users.values()):
            # print(user.posts)
            for post_id in list(user.posts):
                if [0, post_id] not in mas:
                    mas.append([0, post_id])
                # print(post_id)
        print(mas)
        for user in list(self.users.values()):
            for post_id in list(user.read):
                for i in range(len(mas)):
                    if mas[i][1] == post_id:
                        mas[i][0] += 1
        print(mas)
        mas.sort(reverse=True)
        print(mas)
        mas = mas[:k:]
        for i in range(len(mas)):
            mas[i] = mas[i][1]

        for i in self.users:
            if i != 1.1:
                del i
        return mas


class User:

    def __init__(self, user_id):
        self.user_id = user_id
        self.posts = []  # post_id
        self.subscribes = []  # user_id
        self.read = []  # post_id

    def new_subscribe(self, user_id):
        if not (user_id in self.subscribes):
            self.subscribes.append(user_id)

    def new_post(self, post_id):
        if not (post_id in self.posts):
            self.posts.append(post_id)

    def new_read(self, post_id):
        if not (post_id in self.read):
            self.read.append(post_id)


# vk = VKPoster()
# vk.user_follow_for( 15 , 123 )
# vk.user_follow_for( 15 , 1233 )
# vk.user_posted_post( 123 , 4 )
# vk.user_posted_post( 123 , 884 )
# vk.user_posted_post( 123 , 8834 )
# vk.user_posted_post( 123 , 88456 )
# vk.user_posted_post( 1233 , 1 )
# vk.user_posted_post( 1233 , 23 )
# vk.user_posted_post( 1233 , 884568 )
# vk.get_recent_posts( 15 , 4 )
# vk.user_read_post( 15 , 88456 )
# vk.user_read_post( 15 , 8834 )
# vk.user_read_post( 1533 , 8834 )
# vk.user_read_post( 1 , 8834 )
# vk.user_read_post( 2 , 88 )
# vk.user_read_post( 3 , 88 )
# vk.user_read_post( 15 , 123 )
# vk.user_read_post( 15 , 123 )
# vk.user_read_post( 15 , 123 )
# vk.user_read_post( 15 , 123 )
# vk.user_read_post( 15 , 123 )
# vk.get_most_popular_posts( 3 )
# vk.user_follow_for( 1 , 2 )
# vk.user_follow_for( 2 , 3 )
# vk.user_follow_for( 3 , 1 )
# vk.user_posted_post( 1 , 111 )
# vk.user_posted_post( 1 , 112 )
# vk.user_posted_post( 1 , 113 )
# vk.user_posted_post( 1 , 114 )
# vk.user_posted_post( 2 , 222 )
# vk.user_posted_post( 2 , 333 )
# vk.get_recent_posts( 3 , 10 )
# vk.get_recent_posts( 2 , 10 )
# vk.get_recent_posts( 1 , 10 )
# vk.user_posted_post( 1 , 120 )
# vk.user_posted_post( 1 , 121 )
# vk.user_posted_post( 1 , 122 )
# vk.get_recent_posts( 3 , 3 )
# vk.user_follow_for( 3 , 2 )
# vk.get_recent_posts( 3 , 4 )
# vk.user_read_post( 1 , 222 )
# vk.user_read_post( 1 , 333 )
# vk.user_read_post( 3 , 122 )
# vk.user_read_post( 3 , 120 )
# vk.user_read_post( 2 , 120 )
# vk.user_read_post( 3 , 121 )
# vk.user_read_post( 3 , 113 )
# vk.get_most_popular_posts( 3 )