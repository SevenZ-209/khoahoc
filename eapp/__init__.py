from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cloudinary
from flask_login import LoginManager

from cloudinary.uploader import upload

app = Flask(__name__)
app.secret_key='123123213321313213'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:1@localhost/coursedb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 8

cloudinary.config(cloud_name='dgpiotsmt',
                    api_key='641336261286631',
                    api_secret='9IM8MLY8s6Y4Pj6deAJZv6_FhJU')

db = SQLAlchemy(app=app)
login = LoginManager(app=app)
login.login_view = 'login_view'
login.login_message = 'Vui lòng đăng nhập để thực hiện chức năng này!'
login.login_message_category = 'warning'

from eapp import index
