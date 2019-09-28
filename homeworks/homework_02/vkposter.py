from homeworks.homework_02.heap import MaxHeap
from homeworks.homework_02.fastmerger import FastSortedListMerger


class VKPoster:
    def __init__(self):
        self.posts = dict([list[int], int])   # key - post_id, info - list if users who read
        self.users = dict([set[int], list[int]])    # key user_id,info - (set of subscribes, list of added posts)


    def user_posted_post(self, user_id: int, post_id: int):
        self.users[user_id][1].append(post_id)


    def user_read_post(self, user_id: int, post_id: int):
        if user_id not in self.posts[post_id][0]:
            self.posts[post_id][1] + 1
        self.posts[post_id][0].append(user_id)


    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        self.users[follower_user_id][0].add(followee_user_id)


    def get_recent_posts(self, user_id: int, k: int) -> list:
        lol = []  # list of lists
        for val in self.users[user_id][0]:
            lol.append(self.users[val][1])
        return FastSortedListMerger(lol, k)


    def get_most_popular_posts(self, k: int) -> list:
        arr = []
        out_arr = []
        for key in self.posts:
            arr.append(self.posts[key][1], key)
        mh = MaxHeap(arr)
        while len(out_arr) < k and len(mh.array) > 0:
            out_arr.append(mh.extract_maximum()[1])
        return sorted(out_arr)
