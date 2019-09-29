import heapq


class VKPoster:

    def __init__(self):
        self.users_reads = {}
        self.users_posts = {}
        self.users_follows = {}
        self.popular_posts = {}

    def user_posted_post(self, user_id: int, post_id: int):
        """
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        """
        if user_id in self.users_posts:
            self.users_posts[user_id].append(post_id)
        else:
            self.users_posts[user_id] = [post_id]

    def user_read_post(self, user_id: int, post_id: int):
        """
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        """
        if user_id not in self.users_reads or post_id not in self.users_reads[user_id]:
            if post_id in self.popular_posts:
                self.popular_posts[post_id] += 1
            else:
                self.popular_posts[post_id] = 1
            if user_id not in self.users_reads:
                self.users_reads[user_id] = [post_id]
            else:
                self.users_reads[user_id].append(post_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        """
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        """
        if follower_user_id != followee_user_id:
            if follower_user_id not in self.users_follows:
                self.users_follows[follower_user_id] = [followee_user_id]
            else:
                self.users_follows[follower_user_id].append(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int) -> list:
        """
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        """
        new_followee_posts = []
        if user_id not in self.users_follows:
            return new_followee_posts
        else:
            for followee in self.users_follows[user_id]:
                if followee in self.users_posts:
                    new_followee_posts.extend(self.users_posts[followee])
            return sorted(new_followee_posts, reverse=True)[:k]

    def get_most_popular_posts(self, k: int) -> list:
        """
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        """

        list_popular_posts = []
        for key, val in self.popular_posts.items():
            heapq.heappush(list_popular_posts, (val, key))

        return [el[1] for el in heapq.nlargest(k, list_popular_posts)]
