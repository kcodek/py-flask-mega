from app import app,db
from app.models import User, Post

#To run the application you set the FLASK_APP=microblog.py in your terminal session, and then execute flask run. 
#using flask shell, the command pre-imports the application instance.

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'User':User, 'Post':Post }
