from flask import Flask 

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hertz.db'

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT":465, 
    "MAIL_USE_TLS":False, 
    "MAIL_USE_SSL": True, 
    "MAIL_USERNAME": 'gauravgluon20@gmail.com', 
    "MAIL_PASSWORD":'superstringtheory'

}

app.config.update(mail_settings)
mail = Mail(app)

from flask_blog import routes




