class VKPoster:

    def __init__(self):
        self.posts = dict()
        self.reads = dict()
        self.subscriptions = dict()

    def user_posted_post(self, user_id: int, post_id: int):
        if user_id in self.posts:
            self.posts[user_id].append(post_id)
        else:
            self.posts[user_id] = [post_id]
        return None

    def user_read_post(self, user_id: int, post_id: int):
        if (user_id in self.reads) and (post_id not in self.reads[user_id]):
            self.reads[user_id].append(post_id)
        elif user_id not in self.reads:
            self.reads[user_id] = [post_id]
        return None

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if follower_user_id in self.subscriptions:
            self.subscriptions[follower_user_id].append(followee_user_id)
        else:
            self.subscriptions[follower_user_id] = [followee_user_id]
        return None

    def get_recent_posts(self, user_id: int, k: int)-> list:
        out_list = list()
        for i in self.subscriptions[user_id]:
            if i in self.posts:
                tmp = self.posts[i][:-k-1:-1]
                for j in tmp:
                    out_list.append(j)
        out_list = sorted(out_list)[:-k-1:-1]
        return out_list

    def get_most_popular_posts(self, k: int) -> list:
        out_list = list()
        pop_dict = dict()
        for post_list in self.reads.values():
            for post_id in post_list:
                if post_id not in pop_dict:
                    pop_dict[post_id] = 1
                else:
                    pop_dict[post_id] += 1
        k1 = 0
        while len(pop_dict) != 0 and k1 != k:
            max_value = max(pop_dict.values())
            max_list = [k for k, v in pop_dict.items() if v == max_value]
            max_list = sorted(max_list)[::-1]
            for i in max_list:
                if k1 < k:
                    out_list.append(i)
                    k1 += 1
                    del pop_dict[i]
        return out_list
