from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from database import db_manager
import wtforms_json

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
db_cnx_manager = db_manager.DBconnect()
db_connection_string = db_cnx_manager.get_connection_string()
app.config['SQLALCHEMY_DATABASE_URI'] = db_connection_string  # 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
wtforms_json.init()

from flaskdss import routes
