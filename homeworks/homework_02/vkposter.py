#!/usr/bin/env python
# coding: utf-8


class VKPoster:
	def __init__(self):
		self.users = {}
		self.posts = {}
	def user_posted_post(self, user_id: int, post_id: int):
		'''
		Метод который вызывается когда пользователь user_id
		выложил пост post_id.
		:param user_id: id пользователя. Число.
		:param post_id: id поста. Число.
		:return: ничего
		'''
		if post_id not in self.posts:
			self.posts[post_id] = ['creater',0]
		self.posts[post_id][0] = user_id
		return None

	def user_read_post(self, user_id: int, post_id: int):
		'''
		Метод который вызывается когда пользователь user_id
		прочитал пост post_id.
		:param user_id: id пользователя. Число.
		:param post_id: id поста. Число.
		:return: ничего
		'''
		self.posts[post_id].append(user_id)
		self.posts[post_id][1] += 1
		return None

	def user_follow_for(self, follower_user_id: int, followee_user_id: int):
		'''
		Метод который вызывается когда пользователь follower_user_id
		подписался на пользователя followee_user_id.
		:param follower_user_id: id пользователя. Число.
		:param followee_user_id: id пользователя. Число.
		:return: ничего
		'''
		if follower_user_id not in self.users:
			self.users[follower_user_id] = []
		self.users[follower_user_id].append(followee_user_id)
		return None

	def get_recent_posts(self, user_id: int, k: int)-> list:
		'''
		Метод который вызывается когда пользователь user_id
		запрашивает k свежих постов людей на которых он подписан.
		:param user_id: id пользователя. Число.
		:param k: Сколько самых свежих постов необходимо вывести. Число.
		:return: Список из post_id размером К из свежих постов в
		ленте пользователя. list
		'''
		folowee = self.users.get(user_id)
		list_id = []
		for key in self.posts:
			for fol in folowee:
				if self.posts.get(key)[0] == fol:
					list_id.append(key)
		list_id = sorted(list_id)[:k]
		return list_id

	def get_most_popular_posts(self, k: int) -> list:
		'''
		Метод который возвращает список k самых популярных постов за все время,
		остортированных по свежести.
		:param k: Сколько самых свежих популярных постов
		необходимо вывести. Число.
		:return: Список из post_id размером К из популярных постов. list
		'''
		posts_help = list(self.posts.items())
		posts_help.sort(key=lambda i: i[1][1])
		posts_help = posts_help[:k]
		posts_help.sort(key=lambda i: i[0])
		popular_list = []
		for _ in posts_help:
			popular_list.append(_[0])
		return popular_list

a = VKPoster()
a.user_posted_post(21,22)
a.user_posted_post(31,32)
a.user_follow_for(11,21)
a.user_follow_for(11,31)
print(a.get_recent_posts(11,2))





