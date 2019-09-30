class VKPoster:

    def __init__(self):
        self.users = {}
        self.posts = {}

    def user_posted_post(self, user_id: int, post_id: int):
        if user_id not in self.users:
            self.users[user_id] = {'posts': [], 'followees': []}
        self.users[user_id]['posts'].append(post_id)

    def user_read_post(self, user_id: int, post_id: int):
        if post_id in self.posts:
            if user_id not in self.posts[post_id][1:]:
                self.posts[post_id][0] += 1
                self.posts[post_id].append(user_id)
        else:
            self.posts[post_id] = [1, user_id]

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if follower_user_id not in self.users:
            self.users[follower_user_id] = {'posts': [], 'followees': []}
        self.users[follower_user_id]['followees'].append(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int) -> list:
        mat = []
        for user in self.users[user_id]['followees']:
            mat += self.users[user]['posts']
        mat = sorted(mat, reverse=True)
        return mat[:k]

    def get_most_popular_posts(self, k: int) -> list:
        max_id = max(self.posts)
        func = max_id*[0]
        for i in range(1, max_id+1):
            if i in self.posts:
                func[max_id - i] = self.posts[i][0]

        mat = []
        for i in range(k):
            temp = func.index(max(func))
            func[temp] = -1
            mat.append(max_id - temp)

        return mat
