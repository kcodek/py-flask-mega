from flask import Flask
from config import Config

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'you-will-never-guess'
# # ... add more variables here as needed
app.config.from_object(Config)
# print(app.config['SECRET_KEY'])
from app import routes
