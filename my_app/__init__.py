from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.script import Manager
from flask.ext.migrate import MigrateCommand, Migrate
from location.momentjs import momentjs
import os

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
# for heroku
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://idqkyulhtalkgb:zXim5IIGw1PL0iH0dtyvvWaHaX@ec2-54-227-248-123.compute-1.amazonaws.com:5432/dc93nanbifig2k'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dem:123@localhost/lbs2'
app.config['SQLALCHEMY_MIGRATE_REPO'] = os.path.join(basedir, 'db_repository')
app.config['WTF_CSRF_SECRET_KEY'] = 'random key for form'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


app.secret_key = 'some_random_key jkljlkjsdfewef123'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


app.jinja_env.globals['momentjs'] = momentjs


import my_app.location.views

db.create_all()
