#!/usr/bin/env python
# coding: utf-8

class VKPost:
    def __init__(self, post_id: int, user_id: int) -> None:
        self.id = post_id
        self.owner_id = user_id
        self.read_by = dict()

    def readed_by(self, user_id: int) -> None:
        self.read_by[user_id] = None
        return

    @classmethod
    def get_sort_lambda(self, sort_by: str) -> callable:
        sort_key = None
        if sort_by == 'fresh':
            sort_key = lambda p: p.id
        elif sort_by == 'popular':
            sort_key = lambda p: (len(p.read_by), p.id)
        else:
            raise KeyError("unknown sort_by value: {}".format(sort_by))

        return sort_key

class VKUser:
    def __init__(self, user_id: int) -> None:
        self.id = user_id
        self.follows = dict()
        self.posts = dict()

    def follow(self, folowee_id: int) -> None:
        self.follows[folowee_id] = None

        return

    def post(self, post_id: int) -> VKPost:
        post = VKPost(post_id, self.id)
        self.posts[post.id] = post
        return post

    def get_posts(self, limit: int = -1, sort_by: str = 'fresh') -> list:

        sort_key = VKPost.get_sort_lambda(sort_by)
        userposts = list(self.posts.values())
        # print("userposts:", userposts)
        # print('type', type(userposts))
        return sorted(userposts, key=sort_key, reverse=True)[:limit]

class VKPoster:

    def __init__(self):
        # raise NotImplementedError
        self.users = dict()
        self.posts = dict()

    def _get_user(self, user_id: int) -> VKUser:
        if user_id not in self.users:
            self.users[user_id] = VKUser(user_id)
        return self.users.get(user_id, None)

    def _get_post(self, post_id: int) -> VKPost:
        # странно, но ок. по условиям теста пост, который не прочитали должен быть создан.
        if post_id not in self.posts:
            self.posts[post_id] = VKPost(post_id, None)
        return self.posts[post_id]

    def user_posted_post(self, user_id: int, post_id: int) -> None:
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        post = self._get_user(user_id).post(post_id)
        self.posts[post.id] = post

        return

    def user_read_post(self, user_id: int, post_id: int) -> None:
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''

        post = self._get_post(post_id)
        user = self._get_user(user_id)
        post.readed_by(user.id)
        return

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''

        actor = self._get_user(follower_user_id)
        followee = self._get_user(followee_user_id)
        actor.follow(followee.id)
        return

    def _get_sorted_posts(self, user_id: int, limit: str, sort_by: str) -> list:
        user = self._get_user(user_id)
        followee_posts = []
        for followee_id in user.follows:
            followee = self._get_user(followee_id)
            followee_posts += followee.get_posts(limit=limit, sort_by=sort_by)

        return sorted(followee_posts, key=VKPost.get_sort_lambda(sort_by), reverse=True)[:limit]

    def get_recent_posts(self, user_id: int, k: int)-> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. listе
        '''

        return [p.id for p in self._get_sorted_posts(user_id, k, 'fresh')]

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        myposts = list(self.posts.values())
        # print("posts", [(k, len(self.posts[k].read_by))for k in self.posts])
        return [ p.id for p in sorted(myposts, key=VKPost.get_sort_lambda('popular'), reverse=True)[:k]]
