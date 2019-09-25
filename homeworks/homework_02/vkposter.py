#!/usr/bin/env python
# coding: utf-8


#from homeworks.homework_02.heap import MaxHeap
#from homeworks.homework_02.fastmerger import FastSortedListMerger


class VKPoster:

    users = dict()  # key = user_id; value = User

    def __init__(self):
        for i in range(2000):
            self.users[i] = User(i)

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        self.users[user_id].new_post(post_id)

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        self.users[user_id].new_read(post_id)

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        self.users[follower_user_id].new_subscribe(followee_user_id)

    def get_recent_posts(self, user_id: int, k: int)-> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        new_posts = []
        for user in self.users[user_id].subscribes:
            for post_id in self.users[user].posts:
                if not (post_id in new_posts):
                    new_posts.append(post_id)
        new_posts.sort(reverse=True)
        return new_posts[0:k:]

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        mas = list()
        for user in self.users.values():
            for post_id in user.read:
                a = [post_id, 1]
                if len(mas) == 0:
                    mas = [a]
                else:
                    iter = len(mas) - 1
                    while a[0] > mas[iter][0] and iter >= 0:
                        iter -= 1
                    mas.insert(iter, a)
                    for i in range(len(mas)):
                        if mas[i][0] == post_id:
                            mas[i][1] += 1
                            bool_per = True
                            while bool_per:
                                if mas[i][1] == mas[i - 1] and mas[i][0] > mas[i - 1][0]:
                                    mas[i], mas[i - 1] = mas[i - 1], mas[i]
                                else:
                                    bool_per = False
                            break
        mas = mas[:k:]
        for i in range(len(mas)):
            mas[i] = mas[i][0]
        return mas
                # # TODO научить правильно помещать элемент в массив (post_dict заменить на массив массивов из двух элементов)
                # if post_id in post_dict:
                #     post_dict[post_id] += 1
                #
                # else:
                #     post_dict[post_id] = 1
        # tuple_posts = list(post_dict.items())
        # tuple_posts.sort(key=lambda i: i[1], reverse=True)
        # list_post = []
        # keys_posts = [i[0] for i in tuple_posts]
        # iter_one = 0
        # iter_two = 1
        # while iter_two < len(keys_posts):
        #     if iter_two != len(keys_posts)-1 and keys_posts[iter_one] != keys_posts[iter_two]:
        #         iter_one += 1
        #         iter_two += 1
        #     else:
        #         while iter_two != len(keys_posts)-1 and keys_posts[iter_one] == keys_posts[iter_two]:
        #             iter_two += 1
        #     if iter_two != len(keys_posts)-1:
        #         break
        #     prom_list = []
        #     for i in range(iter_one, iter_two):
        #         prom_list.append(tuple_posts[i][0])
        #     list_post += prom_list
        #return list_post[0:k:]

        # for i in range(len(tuple_posts)):
        #     list_post. append([tuple_posts[i][1], tuple_posts[i][0]])

        # popular_posts [просмотры, id] отсортированы по просмотрам по убыванию
        # нужно отсортировать по свежести внутри количества просмотров

        #popular_posts = [post_id for post_id in tuple_posts]

        # popular_posts = sorted(popular_posts, reverse=True)






        # postses = dict()
        # for user_id in self.users.keys():  # ид юзеров в массиве
        #     for post_id in self.users[user_id].read:  # ид постов каждого юзера в массиве
        #         if not (post_id in postses.keys()):  # если данный пост ещё не встречался
        #             postses[post_id] = 1  # то добавь его в список всех со значением 1
        #         else:  # иначе
        #             postses[post_id] += 1  # увеличь число его прочтений на 1
        # list_posts = list(postses.items())  # создаем массив пар (ключ-значение)
        # list_posts.sort(key=lambda i: i[1], reverse=True)  # сортируем по популярности
        # list_posts = list_posts[0:k:]  # оставляем только первые k постов
        # popular_posts = [post_id[0] for post_id in list_posts]
        # return sorted(popular_posts, reverse=True)


class User:

    posts = []  # post_id
    subscribes = []  # user_id
    read = []  # post_id

    def __init__(self, user_id):
        self.user_id = user_id

    def new_subscribe(self, user_id):
        if not (user_id in self.subscribes):
            self.subscribes.append(user_id)

    def new_post(self, post_id):
        if not (post_id in self.posts):
            self.posts.append(post_id)

    def new_read(self, post_id):
        if not (post_id in self.read):
            self.read.append(post_id)
