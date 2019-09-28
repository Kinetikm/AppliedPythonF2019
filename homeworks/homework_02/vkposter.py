#!/usr/bin/env python
# coding: utf-8


class VKPoster:

    def __init__(self):
        self.__user_dict = dict()
        self.__post_dict = dict()
        self.__popularity_list = list()

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if self.__user_dict.get(user_id) is None:
            self.__user_dict.update({user_id: []})
        self.__popularity_list.append([post_id, 0])
        self.__post_dict.update({post_id: [user_id]})

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if self.__post_dict.get(post_id) is None:
            self.__post_dict.update({post_id: [-1]})
            self.__popularity_list.append([post_id, 0])
        if user_id not in self.__post_dict[post_id]:
            self.__post_dict[post_id].append(user_id)
            for pidlist in self.__popularity_list:
                if pidlist[0] == post_id:
                    pidlist[1] += 1
                    break

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if self.__user_dict.get(follower_user_id) is None:
            self.__user_dict.update({follower_user_id: []})
        self.__user_dict[follower_user_id].append(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int) -> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        ret = list()
        cur_id_list = self.__user_dict[user_id]
        for pid in self.__post_dict:
            if self.__post_dict[pid][0] in cur_id_list:
                if user_id not in self.__post_dict[pid]:
                    ret.append(pid)
        ret.sort(reverse=True)
        retlen = min(k, len(ret))
        return ret[:retlen]

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все
        время, остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером k из популярных постов. list
        '''
        ret = list()
        self.__popularity_list.sort(key=lambda tlist: (-tlist[1], -tlist[0]))
        retlen = min(k, len(self.__popularity_list))
        for i in range(retlen):
            ret.append(self.__popularity_list[i][0])
        return ret
