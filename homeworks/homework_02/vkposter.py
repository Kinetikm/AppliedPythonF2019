#!/usr/bin/env python
# coding: utf-8


from homeworks.homework_02.heap import MaxHeap
from homeworks.homework_02.fastmerger import FastSortedListMerger


class VKPoster:

    def __init__(self):
        self.followings = {}
        self.posted_posts = {}
        self.read_posts = {}
        self.full_read_list = {}

    def user_posted_post(self, user_id: int, post_id: int):
        """
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        """
        if user_id in self.posted_posts:
            self.posted_posts[user_id].append(post_id)
        else:
            self.posted_posts.update({user_id: [post_id]})
        if post_id not in self.read_posts:
            self.read_posts.update({post_id: []})
        if post_id not in self.full_read_list:
            self.full_read_list.update({post_id: 0})

    def user_read_post(self, user_id: int, post_id: int):
        """
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        """
        if post_id in self.read_posts:
            if user_id not in self.read_posts[post_id]:
                self.read_posts[post_id].append(user_id)
                self.full_read_list[post_id] += 1
        else:
            self.read_posts.update({post_id: [user_id]})
            self.full_read_list.update({post_id: 1})

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        """
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        """
        if follower_user_id in self.followings:
            self.followings[follower_user_id].append(followee_user_id)
        else:
            self.followings.update({follower_user_id: [followee_user_id]})

    def get_recent_posts(self, user_id: int, k: int) -> list:
        """
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        """
        full_list = []
        if user_id in self.followings:
            for followings in self.followings[user_id]:
                if followings in self.posted_posts:
                    full_list.append(self.posted_posts[followings])
        return FastSortedListMerger.merge_first_k(full_list, k)

    def get_most_popular_posts(self, k: int) -> list:
        """
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        """
        if k < len(self.full_read_list) and k != 0:
            length = k
        else:
            length = len(self.full_read_list)
        output_list = []
        list_of_tuple = []
        for posts, reads in self.full_read_list.items():
            list_of_tuple.append((reads, posts))
        h = MaxHeap(list_of_tuple)
        while len(output_list) != length:
            reads, post = h.extract_maximum()
            output_list.append(post)
        return output_list
