#!/usr/bin/env python
# coding: utf-8


from user import User
from post import Post

class VKPoster:

    def __init__(self):
        self.users_dict = {}
        self.posts_dict = {}

    def get_user(self, user_id):
        if user_id not in self.users_dict:
            user = User(user_id)
            self.users_dict[user_id] = user

        return self.users_dict[user_id]

    def get_post(self, post_id):
        if post_id not in self.posts_dict:
            post = Post(post_id)
            self.posts_dict[post_id] = post

        return self.posts_dict[post_id]

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        user = self.get_user(user_id)
        post = self.get_post(post_id)
        user.posted.add(post)

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        user = self.get_user(user_id)
        post = self.get_post(post_id)
        post.read.add(user)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if followee_user_id != follower_user_id:
            follower = self.get_user(follower_user_id)
            followee = self.get_user(followee_user_id)
            follower.subscriptions.add(followee)

    def get_recent_posts(self, user_id: int, k: int)-> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        user = self.get_user(user_id)
        recent_posts = []
        subs = user.subscriptions
        for sub in subs:
            for available_post in sub.posted:
                recent_posts.append(available_post.id)
        recent_posts.sort(reverse=True)
        recent_posts = recent_posts[0:k] if k <= len(recent_posts) else recent_posts
        return recent_posts

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        most_pop_posts = list(self.posts_dict.keys())
        # по свежести(id)
        most_pop_posts.sort(key=lambda id: id, reverse=True)
        # по количеству прочитавших
        most_pop_posts.sort(key=lambda id: len(self.posts_dict[id].read), reverse=True)
        most_pop_posts = most_pop_posts[0:k] if k <= len(most_pop_posts) else most_pop_posts
        return most_pop_posts
