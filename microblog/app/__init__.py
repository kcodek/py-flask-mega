from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# The Flask-Login extension works with the application's user model, 
# & expects certain properties and methods to be implemented in it
login = LoginManager(app)
'''The 'login' value is the function (or endpoint) name for the login view.
In other words, the name you would use in a url_for() call to get the URL.'''
login.login_view = 'login' 

from app import routes, models

'''
The bottom import is a workaround to circular imports, a common problem with Flask applications. 
You are going to see that the routes module needs to import the app variable defined in this script, 
so putting one of the reciprocal imports at the bottom avoids the error that results from the mutual references between these two files.

'''