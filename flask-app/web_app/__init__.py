from flask import Flask
from config import Config
from flask_login import LoginManager
from rabbit_producer.rabbit_producer import produce_message

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
email_sender = produce_message()

from web_app import tokens
from web_app.storage_manager.storage_manager import StorageManager
USM = StorageManager()

@login_manager.user_loader
def load_user(id):
    return USM.select(int(id), category='id')


from web_app import routes
