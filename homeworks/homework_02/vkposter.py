class VKPoster:

    def __init__(self):
        self.user = {}
        self.post = {}
        self.follow = {}

    def user_posted_post(self, user_id: int, post_id: int):
        if user_id in self.user.keys():
            self.user[user_id].append(post_id)
        else:
            self.user[user_id] = [post_id]

    def user_read_post(self, user_id: int, post_id: int):
        if post_id not in self.post.keys():
            self.post[post_id] = set()
        self.post[post_id].append(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if follower_user_id not in self.follow.keys():
            self.follow.update({follower_user_id: [followee_user_id]})
        else:
            self.follow[follower_user_id].append(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int) -> list:
        list_post = list()
        if user_id in self.follow.keys():
            for i in self.follow[user_id]:
                if i in self.user:
                    list_post.extend(self.user[i])
        list_post.sort(reverse=True)
        return list_post[:k]

    def get_most_popular_posts(self, k: int) -> list:
        list_pop = list()
        for i in self.post.keys():
            list_pop.append((len(self.post[i]), i))
        list_pop = sorted(list_pop, key=lambda f: (f[0], f[1]), reverse=True)
        list_pop = [list_pop[i][1] for i in range(min(k, len(list_pop)))]
        return list_pop
