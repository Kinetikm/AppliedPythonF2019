#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.users_posts = {}
        self.users_reads = {}
        self.users_follows = {}
        self.popular_posts = {}

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        print(f'Useer {user_id} posted {post_id}')
        if user_id not in self.users_posts:
            self.users_posts[user_id] = [post_id]
        else:
            self.users_posts[user_id].append(post_id)

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if (user_id not in self.users_reads) or (post_id not in self.users_reads[user_id]):
            if post_id in self.popular_posts:
                self.popular_posts[post_id] += 1
            else:
                self.popular_posts[post_id] = 1
            self.users_reads[user_id] = [post_id]

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if followee_user_id != follower_user_id:
            if follower_user_id not in self.users_follows:
                self.users_follows[follower_user_id] = [followee_user_id]
            else:
                self.users_follows[follower_user_id].append(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int)-> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        new_posts = []
        for follows in self.users_follows[user_id]:
            if follows in self.users_posts:
                new_posts.extend(self.users_posts[follows])
        return sorted(new_posts, reverse=True)[:k]

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        sort_by_values = sorted(self.popular_posts, key=self.popular_posts.get, reverse=True)
        list_popular_posts = [item for item in sort_by_values][:k]
        for i in range(1, len(list_popular_posts)):
            if self.popular_posts[list_popular_posts[i]] == self.popular_posts[list_popular_posts[i-1]]:
                if list_popular_posts[i] > list_popular_posts[i-1]:
                    list_popular_posts[i], list_popular_posts[i-1] = list_popular_posts[i-1], list_popular_posts[i]
        return list_popular_posts
