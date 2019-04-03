from flask import Flask
from config import Config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


from web_app.storage_manager.storage_manager import StorageManager
USM = StorageManager()

@login_manager.user_loader
def load_user(id):
    return USM.select(int(id), category='id')


from web_app import routes
