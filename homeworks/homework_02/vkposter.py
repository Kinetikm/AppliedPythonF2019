#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.read_users = {}  # все посты post_id:list of user who read
        self.user_posts = {}  # user_id:list(post_id)
        self.user_subscriptions = {}  # user_id:user_subscriptions

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id. поста. Число.
        :return: ничего
        '''
        if user_id in self.user_posts:
            self.user_posts[user_id].append(post_id)
        else:
            self.user_posts[user_id] = [post_id]
        self.read_users[post_id] = []
        print("Adding post: ", post_id, "from user ", user_id)

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if post_id in self.read_users:
            if user_id not in self.read_users[post_id]:
                self.read_users[post_id].append(user_id)
        else:
            self.read_users[post_id] = [user_id]

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id in self.user_subscriptions:
            self.user_subscriptions[follower_user_id].add(followee_user_id)
        else:
            s = set()
            s.add(followee_user_id)
            self.user_subscriptions[follower_user_id] = s

    def get_recent_posts(self, user_id: int, k: int)-> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        recent_posts = []
        for itr in self.user_subscriptions[user_id]:
            if itr not in self.user_posts:
                continue
            recent_posts += self.user_posts[itr]
            recent_posts.sort()
            if len(recent_posts) > k:
                del recent_posts[:len(recent_posts) - k]
        recent_posts = recent_posts[::-1]
        return recent_posts

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        print("All post: ", self.read_users)
        sorting_list = []
        pop_posts = []
        for post_id in self.read_users:
            sorting_list.append((len(self.read_users[post_id]), post_id))
        sorting_list.sort(reverse=True)
        for i in range(k):
            pop_posts.append(sorting_list[i][1])
        print("Actual pop_post", pop_posts)
        return pop_posts
