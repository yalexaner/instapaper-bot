# coding=utf-8

import requests
import pickle
import os


class Instapaper(object):


    def __init__(self, user_id):
        if not os.path.exists('users.pkl'):
            with open('users.pkl', 'wb') as file:
                pickle.dump(dict(), file, pickle.HIGHEST_PROTOCOL)

        with open('users.pkl', 'rb') as file:
            users = pickle.load(file)

        self._username, self._password = users.get(user_id, (None, None))

        self._user_id = user_id
        self._url = 'https://www.instapaper.com/api/'


    def auth(self, username, password) -> int:
        """
        Authorizes user.
        :param username: User's username or email.
        :param password: User's password.
        :return: Status code as an integer (200, 403, 500).
        """
        self._username = username
        self._password = password

        data = {
            'username': username,
            'password': password
        }

        response = requests.get(self._url + 'authenticate', params=data)

        if response.status_code == 200:
            with open('users.pkl', 'rb') as file:
                users = pickle.load(file)

            users[self._user_id] = (username, password)

            with open('users.pkl', 'wb') as file:
                pickle.dump(users, file, pickle.HIGHEST_PROTOCOL)

        return response.status_code


    def add(self, url) -> int:
        """
        Adds url to an Instapaper account.
        :param url: URL that should be saved.
        :return: Status code as an integer (201, 400, 403, 500).
        """
        data = {
            'username': self._username,
            'password': self._password,
            'url': url
        }

        response = requests.get(self._url + 'add', params=data)

        return response.status_code


    def is_authorized(self) -> bool:
        """
        Checks if the user is authorized.
        """
        return True if self._username else None