#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.posts = {}
        self.users = {}
        self.followers = {}

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if user_id not in self.users:
            self.users[user_id] = [post_id]
        else:
            if post_id not in self.users[user_id]:
                self.users[user_id].append(post_id)
                self.posts[post_id] = []
        pass

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if post_id not in self.posts:
            self.posts[post_id] = [user_id]
        else:
            if user_id not in self.posts[post_id]:
                self.posts[post_id].append(user_id)
        pass

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if follower_user_id not in self.followers:
            self.followers[follower_user_id] = [followee_user_id]
        else:
            if followee_user_id not in self.followers[follower_user_id]:
                self.followers[follower_user_id].append(followee_user_id)
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
        recent_posts = []
        for flwe in self.followers[user_id]:
            if flwe in self.users:
                recent_posts = recent_posts + self.users[flwe]
        for post in recent_posts:
            if post in self.posts:
                if user_id in self.posts[post]:
                    recent_posts.remove(post)
        recent_posts.sort(reverse=True)
        return recent_posts[:k]
        pass

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        popular_posts = self.posts.copy()
        for post in popular_posts:
            popular_posts[post] = len(popular_posts[post])
        popular_posts = list(popular_posts.items())
        popular_posts.sort(key=lambda i: i[1])
        popular_posts.reverse()
        top_views_dict = {}
        top_views_list = []
        for i in range(len(popular_posts)):
            if popular_posts[i][1] not in top_views_dict:
                top_views_dict[popular_posts[i][1]] = [popular_posts[i][0]]
                top_views_list.append(popular_posts[i][1])
            else:
                top_views_dict[popular_posts[i][1]].append(popular_posts[i][0])
        for view in top_views_dict:
            top_views_dict[view].sort(reverse=True)
        result = []
        for i in range(len(top_views_list)):
            result = result + top_views_dict[top_views_list[i]]
        return result[:k]
        pass
