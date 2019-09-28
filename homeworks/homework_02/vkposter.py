#!/usr/bin/env python
# coding: utf-8


class VKPoster(object):
    def __init__(self):
        self.read_users = {}   # key - post_id, info - list of users who read
        self.read_amount = {}  # key - post_id, info - number of users who read
        self.subscribes = {}    # key user_id,info - set of subscribes
        self.user_added_posts = {}    # key user_id,info - added posts


    def user_posted_post(self, user_id: int, post_id: int):
        if user_id in self.user_added_posts:
            self.user_added_posts[user_id].append(post_id)
        else:
            self.user_added_posts[user_id] = [post_id]


    def user_read_post(self, user_id: int, post_id: int):
        if post_id in self.read_users:
            if user_id not in self.read_users[post_id]:
                self.read_amount[post_id] += 1
            self.read_users[post_id].append(user_id)
        else:
            self.read_users[post_id] = [user_id]
            self.read_amount[post_id] = 1


    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if follower_user_id in self.subscribes:
            self.subscribes[follower_user_id].add(followee_user_id)
        else:
            s = set()
            s.add(followee_user_id)
            self.subscribes[follower_user_id] = s


    def get_recent_posts(self, user_id: int, k: int) -> list:
        out_list = []
        for val in self.subscribes[user_id]:
            out_list += self.user_added_posts[val]
            out_list.sort()
            if len(out_list) > k:
                del out_list[:len(out_list) - k]
            out_list = out_list[::-1]
        return out_list


    def get_most_popular_posts(self, k: int) -> list:
        sort_list = []
        out_list = []
        for key in self.read_amount:
            sort_list.append((key, self.read_amount[key]))
            sort_list.sort(key=lambda x: x[1])
            if len(sort_list) > k:
                del sort_list[:len(out_list) - k - 1]
        for i in range(k):
            out_list.append(sort_list[i][0])
        out_list.sort()
        out_list = out_list[::-1]
        return out_list
