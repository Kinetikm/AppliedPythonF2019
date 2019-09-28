class VKPoster:

    def __init__(self):
        self.users, self.posts = {}, {}

    def invert_dict(self, source_dict):
        res = {}
        for x in source_dict.keys():
            if res.get(source_dict.get(x)['readers']) is None:
                res[source_dict.get(x)['readers']] = x
            elif isinstance(res.get(source_dict.get(x)['readers']), list):
                res[source_dict.get(x)['readers']] += [x]
            else:
                res[source_dict.get(x)['readers']] = \
                    [res.get(source_dict.get(x)['readers']), x]

        return res

    def user_posted_post(self, user_id: int, post_id: int):
        if user_id not in self.users:
            self.users[user_id] = {'publicated': [post_id], 'follow': []}
        else:
            self.users[user_id]['publicated'].append(post_id)
        self.posts[post_id] = {'author': user_id, 'readers': 0, 'people': []}

    def user_read_post(self, user_id: int, post_id: int):
        if post_id not in self.posts:
            self.posts[post_id] = {'author': -1, 'readers': 1,
                                   'people': [user_id]}
        else:
            if user_id not in self.posts[post_id]['people']:
                self.posts[post_id]['readers'] += 1
                self.posts[post_id]['people'].append(user_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        if follower_user_id in self.users:
            self.users[follower_user_id]['follow'].append(followee_user_id)
        else:
            self.users[follower_user_id] = {'publicated': [],
                                            'follow': [followee_user_id]}

    def get_recent_posts(self, user_id: int, k: int) -> list:
        i, return_list, tmp_list = 0, [], [i for i in self.posts.keys()]
        tmp_list.sort(reverse=True)
        for post in tmp_list:
            if i >= k:
                return_list.sort(reverse=True)
                return return_list
            if self.posts[post]['author'] in self.users[user_id]['follow']:
                return_list.append(post)
                i += 1
        return_list.sort(reverse=True)
        return return_list

    def get_most_popular_posts(self, k: int) -> list:
        result, cur = [], k
        temp_posts = self.invert_dict(self.posts)
        print(temp_posts)
        second_tmp = [(j, temp_posts[j]) for j in [i for i in
                                                   temp_posts.keys()][::-1]]
        second_tmp.sort(reverse=True)
        print(second_tmp)
        for tmp in second_tmp:
            if isinstance(tmp[1], list):
                tmp[1].sort(reverse=True)
                result += tmp[1][:cur]
                if len(result) == k:
                    return result
                else:
                    cur -= len(tmp[1])
            else:
                result.append(tmp[1])
                if len(result) == k:
                    return result
                else:
                    cur -= 1
        return result
