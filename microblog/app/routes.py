from app import app,db  # imports the app variable that is a member of the app package
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from flask import request
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
    # user = {'username': 'Miguel'}
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
    return render_template('index.html', title="Home", posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''The current_user variable comes from Flask-Login and can be used at any time
    during the handling to obtain the user object that represents the client of the req'''
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        '''login_user will register the user as logged in, so that means that
         any future pages the user navigates to will have the current_user variable set to that user.'''            
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        '''
        If the user navigates to /index, for example, the @login_required decorator 
        will intercept the request and respond with a redirect to /login, 
        but it will add a query string argument to this URL, making the complete redirect URL /login?next=/index. 
        The next query string argument is set to the original URL, so the application can use that to redirect back after login.
        '''
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)