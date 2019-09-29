#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.Posts = {}  # Посты id-postid
        self.Follows = {}
        self.post_likes = {}  # postid->likes

    def user_posted_post(self, user_id: int, post_id: int):
        if user_id not in self.Posts:
            self.Posts[user_id] = []
        self.Posts[user_id].append(post_id)

    def user_read_post(self, user_id: int, post_id: int):
        if post_id not in self.post_likes:
            self.post_likes[post_id] = []
        if user_id not in self.post_likes[post_id]:
            self.post_likes[post_id].append(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if followee_user_id != follower_user_id:
            if follower_user_id not in self.Follows:
                self.Follows[follower_user_id] = []
            self.Follows[follower_user_id].append(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int) -> list:
        new_posts = []
        for id in self.Follows[user_id]:
            if id in self.Posts:
                new_posts += self.Posts[id][:-k - 1:-1]
        new_posts.sort()
        return new_posts[:-k - 1:-1]
        '''new_posts.extend(self.Posts[usrId] for usrId in self.Follows[user_id] if usrId in self.Posts)
        return sorted(new_posts, reverse=True)[:k]'''

    def get_most_popular_posts(self, k: int) -> list:
        array = list(self.post_likes.items())
        array.sort(key=lambda val: (len(val[1]), val[0]))
        array = array[:-k - 1:-1]
        return [x[0] for x in array]
