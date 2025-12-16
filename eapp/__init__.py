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

#res = upload('D:\\khoahoc\\eapp\\image\\unavatar.jpg')
#response = cloudinary.uploader.upload_image()
#print(res)

db = SQLAlchemy(app=app)
login = LoginManager(app=app)

# from eapp import models