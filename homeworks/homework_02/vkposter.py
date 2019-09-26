#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        ''' словарь, ключами которого являются id пользователей, а значенями -
            списки с id пользователей, на которых они подписаны '''
        self.users = {}
        ''' словарь, ключами которого являются id постов, а значениями -
            списки с id пользователей, которые его прочитали, причем
            на первом месте стоит создатель поста '''
        self.posts = {}

    def create_new_user(self, user_id):
        self.users.update({user_id: []})

    def user_posted_post(self, user_id: int, post_id: int):
        if self.users.get(user_id) is None:
            self.create_new_user(user_id)
        self.posts.update({post_id: [user_id]})

    def user_read_post(self, user_id: int, post_id: int):
        if self.posts.get(post_id) is None:
            self.posts.update({post_id: ['somebody']})
        if user_id not in self.posts[post_id]:
            self.posts[post_id].append(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if self.users.get(follower_user_id) is None:
            self.create_new_user(follower_user_id)
        if self.users.get(follower_user_id) is None:
            self.create_new_user(followee_user_id)
        self.users[follower_user_id].append(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int) -> list:
        result_list = []
        for post_id in self.posts.keys():
            if self.posts[post_id][0] in self.users[user_id]:
                if user_id not in self.posts[post_id]:
                    result_list.append(post_id)
        result_list = sorted(result_list, key=lambda post_id: -post_id)
        if k < len(result_list):
            return result_list[:k]
        return result_list

    def get_most_popular_posts(self, k: int) -> list:
        result_list = []
        for post_id in self.posts.keys():
            result_list.append((len(self.posts[post_id])-1, post_id))
        result_list = sorted(result_list, key=lambda tup: (-tup[0], -tup[1]))
        result_list = result_list[:min(k, len(result_list))]
        return [tup[1] for tup in result_list]
