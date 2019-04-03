from datetime import datetime
from flask_login import UserMixin
from web_app import login_manager
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin):

    def __init__(self, login, email):
        self.login = login
        self.email = email
        self.confirmed = False
        self.id = 0  # by default

    def set_password(self, password):
        self.hash_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hash_password, password)

    def confirm(self):
        self.confirmed = True

    def is_confirmed(self):
        return self.confirmed
