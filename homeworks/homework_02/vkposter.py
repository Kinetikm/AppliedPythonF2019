#!/usr/bin/env python
# coding: utf-8
from queue import PriorityQueue


class Post:
    '''
    :atribute post_id: id поста
    :atribute read: сколько пользователдей прочли этот пост
    '''
    def __init__(self, post_id: int):
        self.post_id = post_id
        self.read = set()

class User:
    '''
    :atribute user_id: id пользователя
    :atribute posts: какие потсы опубликовал пользователь
    :atribute follows: подписки пользователя
    '''
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.posts = list()
        self.follows = set()

class VKPoster:
    def __init__(self):
        self._users = dict()
        self._posts = dict()

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self._users:
            self._users.update({user_id: User(user_id)})

        self._users[user_id].posts.append(post_id)

        self._posts.update({post_id: Post(post_id)})

        return

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self._users:
            self._users.update({user_id: User(user_id)})
        if post_id not in self._posts:
            self._posts.update({post_id: Post(post_id)})

        self._posts[post_id].read.add(user_id)

        return

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id not in self._users:
            self._users.update({follower_user_id: User(follower_user_id)})
        if followee_user_id not in self._users:
            self._users.update({followee_user_id: User(followee_user_id)})

        self._users[follower_user_id].follows.add(followee_user_id)

        return

    def get_recent_posts(self, user_id: int, k: int) -> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        if user_id not in self._users:
            self._users.update({user_id: User(user_id)})
            return []

        recent_posts = []
        for follow_id in self._users[user_id].follows:
            recent_posts += self._users[follow_id].posts[-k:]

        recent_posts.sort()

        return recent_posts[-k:][::-1]

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        queue = PriorityQueue()
        popular_posts = []
        for post in self._posts.values():
            queue.put(((-len(post.read), -post.post_id), post.post_id))

        for _ in range(k):
            if queue.empty():
                return []
            popular_posts.append(queue.get()[1])

        return popular_posts
