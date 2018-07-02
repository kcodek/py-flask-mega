from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {"username":"Miguel"}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

    return render_template('index.html', title='Home', user=user, posts=posts)


# without using templates
# def index():
#     user = {'username':'Miguel'}
#     return '''
#     <html>
#         <head>
#             <title>Home Page - Microblog</title>
#         </head>
#         <body>
#             <h1>Hello, ''' + user['username'] + '''!</h1>
#         </body>
#     </html>'''