#!/usr/bin/env python
import psycopg2
import time


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
                    email VARCHAR(128), hash_password CHAR(128), \
                    confirmed BOOLEAN)')
            except psycopg2.Error:
                print('Database error, reconnecting')
                self._connect()
            else:
                break

    def insert(self, login, email, hash_password, confirmed):
        while True:
            try:
                cursor = self.conn.cursor()
                cursor.execute('INSERT INTO users(login, email, hash_password, confirmed) \
                VALUES (%s, %s, %s, %s)', (login, email, hash_password, bool(int(confirmed))))
                self.conn.commit()
            except psycopg2.Error:
                print('Database error, reconnecting')
                time.sleep(1)
                self._connect()
            else:
                break

    def select(self, login):
        while True:
            try:
                cursor = self.conn.cursor()
                cursor.execute('SELECT * FROM users WHERE login = %s', (login,))
                self.conn.commit()
                fetch = cursor.fetchall()
                return fetch
            except psycopg2.Error:
                print('Database error, reconnecting')
                time.sleep(1)
                self._connect()
            else:
                break
