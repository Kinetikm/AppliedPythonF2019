from collections import defaultdict
from itertools import chain


class VKPoster:
    def __init__(self):
        self.user_posts = defaultdict(set)
        self.user_followees = defaultdict(set)
        self.post_views = defaultdict(set)

    def user_posted_post(self, user_id, post_id):
        self.user_posts[user_id].add(post_id)

    def user_read_post(self, user_id, post_id):
        self.post_views[post_id].add(user_id)

    def user_follow_for(self, user_id, followee_id):
        self.user_followees[user_id].add(followee_id)

    def get_recent_posts(self, user_id, limit=5):
        followees = self.user_followees[user_id]
        followees_posts = map(self.user_posts.__getitem__, followees)
        posts = list(chain.from_iterable(followees_posts))
        posts.sort(reverse=True)
        return posts[:limit]

    def get_most_popular_posts(self, limit=5):
        posts = self.post_views.keys()
        posts.sort(
            key=lambda post_id: len(self.post_views[post_id]),
            reverse=True,
        )
        return posts[:limit]
