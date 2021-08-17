from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from database import db_manager
import wtforms_json
import os

application = Flask(__name__)
application.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
db_cnx_manager = db_manager.DBconnect()
db_connection_string = db_cnx_manager.get_connection_string()
application.config['SQLALCHEMY_DATABASE_URI'] = db_connection_string  # 'sqlite:///site.db'
db = SQLAlchemy(application)
login_manager = LoginManager(application)
wtforms_json.init()
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

from flaskdss import routes
