class VKPoster:

    def __init__(self,):
        self.user_posts = {}
        self.user_views = {}
        self.user_follows = {}
        self.post_views = {}
        self.recent_posts = []
        self.lst = []

    def user_posted_post(self, user_id: int, post_id: int):
        try:
            self.user_posts[user_id].add(post_id)
        except KeyError:
            self.user_posts[user_id] = {post_id}
        return

    def user_read_post(self, user_id: int, post_id: int):
        if post_id not in self.post_views:
            self.post_views[post_id] = 1
        else:
            self.post_views[post_id] = self.post_views[post_id] + 1
        '''
        post --> число просмотров для постов
        '''
        try:
            self.user_views[user_id].add(post_id)
        except KeyError:
            self.user_views[user_id] = {post_id}
        return

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        try:
            if followee_user_id not in self.user_follows[follower_user_id]\
                    or follower_user_id != followee_user_id:
                self.user_follows[follower_user_id].add(followee_user_id)
        except KeyError:
            if follower_user_id != followee_user_id:
                self.user_follows[follower_user_id] = {followee_user_id}
        return
    
    def get_recent_posts(self, user_id: int, k: int) -> list:
        ls = []
        for i in self.user_follows[user_id]:
            try:
                ls += self.user_posts[i]
            except KeyError:
                continue
        l= sorted(list(set(ls)), reverse=True)
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
