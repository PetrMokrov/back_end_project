#!/usr/bin/env python
import psycopg2
import time
from ..models import User


class StorageManager:

    def __init__(self):
        self.conn = None
        self._connect()
        self._create_table()

    def _connect(self):
        while True:
            try:
                self.conn = psycopg2.connect(
                    host='storage',
                    database='app_storage',
                    user='admin',
                    password='admin'
                )
            except psycopg2.Error:
                print('Cannot connect to database, sleeping 3 seconds')
                time.sleep(3)
            else:
                break

    def _create_table(self):
        while True:
            try:
                cursor = self.conn.cursor()
                cursor.execute('CREATE TABLE IF NOT EXISTS users \
                    (id SERIAL PRIMARY KEY, login VARCHAR(128), \
                    email VARCHAR(128), hash_password VARCHAR(132), \
                    confirmed BOOLEAN)')
            except psycopg2.Error:
                print('Database error, reconnecting')
                self._connect()
            else:
                break

    def insert(self, user):
        '''
        If insert is success, the function returns true,
        Else, it returns false
        '''
        while True:
            try:
                if self.select(user.login, category='login') is not None:
                    return False
                cursor = self.conn.cursor()
                cursor.execute('INSERT INTO users(login, email, hash_password, confirmed) \
                VALUES (%s, %s, %s, %s)', (user.login, user.email, user.hash_password, user.confirmed))
                self.conn.commit()
                return True
            except psycopg2.Error:
                print('Database error, reconnecting')
                time.sleep(1)
                self._connect()
            else:
                break

    def select(self, value, category='login'):
        '''
        The function returns None, if there is no user with very value of
        category, else it returns User instance
        '''
        while True:
            try:
                cursor = self.conn.cursor()
                cursor.execute('SELECT * FROM users WHERE %s = %%s' % category, (value,))
                self.conn.commit()
                fetch = cursor.fetchall()
                if len(fetch) == 0:
                    return None
                user = User(fetch[0][1], fetch[0][2])
                user.id = fetch[0][0]
                user.hash_password = fetch[0][3]
                user.confirmed = fetch[0][4]
                return user
            except psycopg2.Error:
                print('Database error, reconnecting')
                time.sleep(1)
                self._connect()
            else:
                break

    def confirm(self, value, category='login'):
        '''
        The function sets \'confirmed\' parameter of the user with very value
        of category as True\n
        If such user not found, returns False, else returns True
        '''
        while True:
            try:
                if self.select(value, category=category) is not None:
                    return False
                cursor = self.conn.cursor()
                cursor.execute('UPDATER users SET confirmed = TRUE WHERE %s = %%s' % category, (value,))
                self.conn.commit()
                return True
            except psycopg2.Error:
                print('Database error, reconnecting')
                time.sleep(1)
                self._connect()
            else:
                break
