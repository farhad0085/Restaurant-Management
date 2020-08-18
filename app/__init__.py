from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)

migrate = Migrate(app, db)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.login_view = 'main.login'
login_manager.login_message_category = 'warning'

from app.main.routes import main
from app.admin.routes import admin
from app.api.routes import api

app.register_blueprint(main)
app.register_blueprint(api)
