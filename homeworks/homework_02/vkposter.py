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

    def get_most_popular_posts(self, k: int) -> list:
        l = {}
        ls = []
        q = []
        for x in self.read_id:
            if len(self.read_id[x]) not in l:
                l[len(self.read_id[x])] = [x]
            else:
                l[len(self.read_id[x])] += [x]
            l[len(self.read_id[x])].sort(reverse=True)
            if len(self.read_id[x]) not in ls:
                ls.append(len(self.read_id[x]))
        ls.sort(reverse=True)
        for i in ls:
            for j in l[i]:
                if (len(q) != k):
                    q.append(j)
                else:
                    break
        return q
    
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
        for x in range(k)
            ql.append(q[x][1])
        return ql
