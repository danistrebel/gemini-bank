from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import logging
from logging.handlers import RotatingFileHandler


app = Flask(__name__)
app.config["SECRET_KEY"] = "my-security-key"
# Use an absolute path to ensure the database is always in the project folder
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "mybank.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# Logging Configuration
if not os.path.exists('logs'):
    os.mkdir('logs')

file_handler = RotatingFileHandler('logs/gemini_bank.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Gemini Bank startup')

db = SQLAlchemy(app)

login = LoginManager()
login.init_app(app)


from routes import *

if __name__ == '__main__':
    app.run(debug=True)
