from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail, Message

app = Flask(__name__)


app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = '', # Enter email_id and password to setup with smtp server
	MAIL_PASSWORD = ''	# Enter app password of 16 digit from  your google account
	)


app.secret_key = ""
app.config['SQLALCHEMY_DATABASE_URI'] = ''   

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite3' 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


from app import view      

