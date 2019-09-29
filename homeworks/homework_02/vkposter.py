#!/usr/bin/env python
# coding: utf-8


# первый лист - собственный пост; второй лист - подписчики; третий - прочитанные посты; четвертый - подписки


class VKPoster:

    def __init__(self):
        self.post_relationship = {}
        self.posts = {}

    def user_posted_post(self, user_id: int, post_id: int):
        self.post_id = post_id
        self.user_id = user_id
        self.posts[post_id] = []
        if user_id not in self.post_relationship:
            self.post_relationship[user_id] = [[], [], [], []]
            self.post_relationship[user_id][0].append(post_id)
        else:
            self.post_relationship[user_id][0].append(post_id)

    def user_read_post(self, user_id: int, post_id: int):
        self.post_relationship[user_id][2].append(post_id)
        if user_id not in self.posts[post_id]:
            self.posts[post_id].append(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        self.post_relationship[follower_user_id][3].append(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int)-> list:
        temp = []
        for i in self.post_relationship[user_id][3]:
            for j in self.post_relationship[i][0]:
                temp.append(j)
        temp.sort()
        return temp[len(temp)-1-k::]

    def get_most_popular_posts(self, k: int) -> list:
        list_d = list(self.posts.items())
        list_d.sort(key=lambda x: len(x[1]), reverse=True)
        temp = [i[0] for i in list_d[:k]]
        return temp

    def print_VK(self):
        print("self.post_relationship: ", self.post_relationship, "\n", "self.posts: ", self.posts, "\n\n")
