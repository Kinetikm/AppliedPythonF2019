class VKPoster:

    def __init__(self,):
        self.user_posts = {}
        self.user_views = {}
        self.user_follows = {}
        self.post_views = {}

    def user_posted_post(self, user_id: int, post_id: int):
        if user_id not in self.user_posts:
            self.user_posts[user_id] = [post_id]
        else:
            self.user_posts[user_id].append(post_id)
        return None

    def user_read_post(self, user_id: int, post_id: int):
        if post_id not in self.user_views:
            self.user_views[post_id] = {user_id}
        else:
            self.user_views[post_id].add(user_id)
        return None

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if follower_user_id not in self.user_follows:
            self.user_follows[follower_user_id] = {followee_user_id}
        else:
            self.user_follows[follower_user_id].add(followee_user_id)
        return None
    
    def get_recent_posts(self, user_id: int, k: int) -> list:
        ls = []
        for i in self.user_follows[user_id]:
            try:
                ls += self.user_posts[i]
            except KeyError:
                continue
        l = sorted(list(set(ls)), reverse=True)
        return l[:k]

    def get_most_popular_posts(self, k: int) -> list:
        q = []
        ql = []
        if k > len(self.post_views):
            k = len(self.post_views)
        for x in range(k):
            q.append(list(self.post_views.items())[x][::-1])
        q.sort()
        q.reverse()
        for x in range(k):
            ql.append(q[x][1])
        return ql
