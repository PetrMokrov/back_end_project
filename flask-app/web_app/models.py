from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from web_app import login_manager


class User(UserMixin):

    def __init__(self, login, email):
        self.login = login
        self.email = email
        self.confirmed = False
        self.id = 0 # by default

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def confirm(self):
        self.confirmed = True
    
    def is_confirmed(self):
        return self.confirmed



class StorageManager:
    id = 0

    def __init__(self):
        self.bd = {}
    
    def insert(self, login, email, password, confirmed):

        inserted_data = {
            'id': self.id,
            'login': login,
            'email': email,
            'password': password,
            'confirmed': confirmed
        }
        self.bd[self.id] = inserted_data
        self.id += 1
    
    def select(self, val, field='login'):
        res = []
        for item in self.bd.items():
            if item[1][field] == val:
                user = (item[0], item[1]['login'], item[1]['email'], item[1]['password'], item[1]['confirmed'])
                res.append(user)
        
        return res

class UserStorageManager(StorageManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def insert(self, User):
        '''
        If insert is success, the function returns true,
        Else, it returns false
        '''
        select_result = super().select(User.login, field='login')
        if(len(select_result) == 0):
            super().insert(User.login, User.email, User.password_hash, User.confirmed)
            return True
        
        return False

    def select_login(self, login):
        '''
        The function returns None, if there is not user with very login,
        else it returns User instance
        '''
        select_result = super().select(login, field='login')
        if(len(select_result) == 0):
            return None
        
        if len(select_result) > 1:
            raise Exception("more then one user with the login")
        
        user_tuple = select_result[0]
        user = User(user_tuple[1], user_tuple[2])
        user.password_hash = user_tuple[3]
        user.confirmed = user_tuple[4]
        user.id = user_tuple[0]
        return user
    
    def select_id(self, id):
        select_result = super().select(id, field='id')
        if(len(select_result) == 0):
            return None
        
        if len(select_result) > 1:
            raise Exception("more then one user with the login")
        
        user_tuple = select_result[0]
        user = User(user_tuple[1], user_tuple[2])
        user.password_hash = user_tuple[3]
        user.confirmed = user_tuple[4]
        user.id = user_tuple[0]
        return user





    

