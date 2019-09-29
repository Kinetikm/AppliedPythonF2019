class VKPoster:

    def __init__(self,):
        self.user_posts = {}
        self.user_views = {}
        self.user_follows = {}
        self.sequence_of_user_posts = []
        self.post_views = {}
        self.recent_posts = []
        self.lst = []

    def user_posted_post(self, user_id: int, post_id: int):
        try:
            self.sequence_of_user_posts.index(post_id)
        except ValueError:
            self.sequence_of_user_posts.append(post_id)
        '''
        sequence_of_user_posts --> последовательность добавленных постов(list)
        '''
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
        for j in range(k):
            for i in self.user_follows[user_id]:
                if self.sequence_of_user_posts[::-1][j] in self.user_posts[i]:
                    if self.sequence_of_user_posts[::-1][j] in self.recent_posts:
                        continue
                    else:
                        self.recent_posts.append(self.sequence_of_user_posts[::-1][j])
                else:
                    self.recent_posts.append(self.sequence_of_user_posts[::-1][j])
        return self.recent_posts

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
