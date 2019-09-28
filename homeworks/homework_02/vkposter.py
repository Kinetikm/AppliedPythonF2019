class VKPoster(object):
    def __init__(self):
        self.posts = dict([list[int], int])   # key - post_id, info - list if users who read
        self.users = dict([set[int], list[int]])    # key user_id,info - (set of subscribes, list of added posts)


def user_posted_post(self, user_id: int, post_id: int):
    self.users[user_id][1].append(post_id)


def user_read_post(self, user_id: int, post_id: int):
    if self.posts.get(post_id) is not None:
        if user_id not in self.posts[post_id][0]:
            self.posts[post_id][1] += 1
        self.posts[post_id][0].append(user_id)


def user_follow_for(self, follower_user_id: int, followee_user_id: int):
    self.users[follower_user_id][0].add(followee_user_id)


def get_recent_posts(self, user_id: int, k: int) -> list:
    out_list = []
    for val in self.users[user_id][0]:
        out_list += self.users[val][1]
        out_list.sort()
        if len(out_list) > k:
            del out_list[:k]
    return out_list


def get_most_popular_posts(self, k: int) -> list:
    sort_list = []
    out_list = []
    for key in self.posts:
        sort_list.append((key, self.posts[key][1]))
        sort_list.sort(key=lambda x: x[1])
        if len(sort_list) > k:
            del sort_list[:k]
    for i in range(k):
        out_list.append(sort_list[i][0])
    return sorted(out_list)








