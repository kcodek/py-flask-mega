#### 01. Hello World
* virtualenv 
    - $ python3 -m venv venv
    - $ source venv/bin/activate
    - $ deactivate


* app = Flask(__name__) 
    - The script above simply creates the application object as an instance of class Flask imported from the flask package. The `__name__` variable passed to the Flask class is a Python predefined variable, which is set to the name of the module in which it is used.

* The routes are the different URLs that the application implements. In Flask, handlers for the application routes are written as Python functions, called view functions. View functions are mapped to one or more route URLs so that Flask knows what logic to execute when a client requests a given URL.

* set the env variable : `export FLASK_APP=microblog.py`
    - $ flask run

* $ pip install python-dotenv  
    - .flaskenv  
        - FLASK_APP=microblog.py

#### 02.Templates
* Creating mock objects is a useful technique that allows you to concentrate on one part of the application without having to worry about other parts of the system that don't exist yet. 
    -   user = {'username': 'Miguel'}
* jinja2
* render_template
* {{}}, {% %}  - dynamic content, loops, conditionals
* template inheritance - {% extends ... %} {% block content %}{% endblock %}

#### 03.Web Forms
* Flask-WTF extension - is a thin wrapper around the WTForms package that nicely integrates it with Flask. $ pip install flask-wtf
* The most basic option to specify configuration options is to  define your variables as keys in app.config, which uses a dictionary style to work with variables - `app.config['SECRET_KEY'] = 'you-will-never-guess'`
* The configuration settings are defined as class variables inside the Config class. Allows to keep configuration in a separate file (Separation of concerns)
*  The Flask-WTF extension uses SECRECT_KEY to protect web forms against a nasty attack called Cross-Site Request Forgery or CSRF (pronounced "seasurf").

* A form class simply defines the fields of the form as class variables.

* Most Flask extensions use a flask_<name> naming convention for their top-level import symbol. In this case, Flask-WTF has all its symbols under flask_wtf.

*  The `action` attribute of the form is used to tell the browser the URL that should be used when submitting the information the user entered in the form. *When the action is set to an empty string the form is submitted to the URL that is currently in the address bar, which is the URL that rendered the form on the page.*

* The `form.hidden_tag()` template argument generates a hidden field that includes a token that is used to protect the form against CSRF attacks. All you need to do to have the form protected is include this hidden field and have the SECRET_KEY variable defined in the Flask configuration. If you take care of these two things, Flask-WTF does the rest for you.

* The fields from the form object know how to render themselves as HTML. All I needed to do was to include {{ form.<field_name>.label }} where I wanted the field label, and {{ form.<field_name>() }} where I wanted the field. For fields that require additional HTML attributes, those can be passed as arguments. The username and password fields in this template take the size as an argument that will be added to the <input> HTML element as an attribute. 

* add a new view function in routes.py

* Receiving Form Data
    - `methods` argument in the route decorator. This tells Flask that this view function accepts GET and POST requests, overriding the default, which is to accept only GET requests.

* The `form.validate_on_submit()` method does all the form processing work. When the browser sends the GET request to receive the web page with the form, this method is going to return False, so in that case the function skips the if statement and goes directly to render the template in the last line of the function.

* The `flash()` function is a useful way to show a message to the user. A lot of applications use this technique to let the user know if some action has been successful or not. The second new function used in the login view function is `redirect()`. This function instructs the client web browser to automatically navigate to a different page, given as an argument. This view function uses it to redirect the user to the index page of the application.

* When you call the `flash()` function, Flask stores the message, but flashed messages will not magically appear in web pages. *The templates of the application need to render these flashed messages in a way that works for the site layout.*

* An interesting property of these flashed messages is that once they are requested through the get_flashed_messages function they are removed from the message list, so they appear only once after the flash() function is called.

* Improving Field Validation
    -  The way the application deals with invalid form input is by re-displaying the form, to let the user make the necessary corrections. The form validators generate these descriptive error messages already, so all that is missing is some additional logic in the template to render them

* Generating Links
    - Instead of writing links directly, Flask provides a function called `url_for()`, which generates URLs using its internal mapping of URLs to view functions. 
    - The argument to url_for() is the endpoint name, which is the name of the view function.  For example, url_for('login') returns /login, and url_for('index') return '/index



#### 04.Database
* The nice thing about `SQLAlchemy` is that it is an ORM not for one, but for many relational databases. SQLAlchemy supports a long list of database engines, including the popular MySQL, PostgreSQL and SQLite. 

* RDBMS are centered around structured data, so when the structure changes the data that is already in the database needs to be migrated to the modified structure.

* The Flask-SQLAlchemy extension takes the location of the application's database from the SQLALCHEMY_DATABASE_URI configuration variable.

* import the module &  add a 'db' object that represents the database . Same thing for 'migrate'

* The data that is stored in the database will be represented by a collection of classes, usually called database models. The ORM layer within SQLAlchemy will do the translations required to map objects created from these classes into rows in the proper database tables.

* The 'User' class created above inherits from db.Model, a base class for all models from Flask-SQLAlchemy. This class defines several fields as class variables. 
Fields are created as instances of the `db.Column` class, which takes the field type as an argument, plus other optional arguments that, for example, allow me to indicate which fields are `unique` and `indexed`, which is important so that database searches are efficient.

* The `__repr__` method tells Python how to print objects of this class, which is going to be useful for debugging. 

* The model class created in the previous section defines the initial database structure (or schema) for this application. But as the application continues to grow, there is going to be a need change that structure, very likely to add new things, but sometimes also to modify or remove items. Alembic (the migration framework used by Flask-Migrate) will make these schema changes in a way that does not require the database to be recreated from scratch.

* To accomplish this seemingly difficult task, Alembic maintains a migration repository, which is a directory in which it stores its migration scripts. Each time a change is made to the database schema, a migration script is added to the repository with the details of the change. To apply the migrations to a database, these migration scripts are executed in the sequence they were created.
    $ flask db init

* The `flask db migrate` command does not make any changes to the database, it just generates the migration script. To apply the changes to the database, the `flask db upgrad`e command must be used.

* But with database migration support, after you modify the models in your application you generate a new migration script (`flask db migrate`), you probably review it to make sure the automatic generation did the right thing, and then apply the changes to your development database (`flask db upgrade`). You will add the migration script to source control and commit it. `flask db downgrade` command, which undoes the last migration

*   1. A new database migration needs to be generated - `$ flask db migrate -m "posts table"`
    2. And the migration needs to be applied to the database - `$ flask db upgrade`
    3. If you are storing your project in source control, also remember to add the new migration script to it.



* All models have a query attribute that is the entry point to run database queries. 
    - `all` - returns all elements of that class, User.query.all()
    - `get` - User.query.get(1)

* `$ flask shell` - the command pre-imports the application instance.
    The nice thing about flask shell is not that it pre-imports app, but that you can configure a "shell context", which is a list of other symbols to pre-import.

*   The `app.shell_context_processor` decorator registers the function as a shell context function. When the flask shell command runs, it will invoke this function and register the items returned by it in the shell session. The reason the function returns a dictionary and not a list is that for each item you have to also provide a name under which it will be referenced in the shell, which is given by the dictionary keys.

#### 05.User Logins
*  Flask-Login provides a mixin class called UserMixin that includes generic implementation of four required items -  is_authenticated, is_active , is_anonymous, get_id()

* Flask-Login keeps track of the logged in user by storing its unique identifier in Flask's user session, a storage space assigned to each user who connects to the application.

* The user loader is registered with Flask-Login with the `@login.user_loader` decorator. 

* The way Flask-Login protects a view function against anonymous users is with a decorator called `@login_required`.

#### 06.Profile page & avatars
* The `@before_request` decorator from Flask register the decorated function to be executed right before the view function.

#### 07.Error Handling
* To run in debug mode - `$ export FLASK_DEBUG=1`. reloader is enabled in debug mode
* To declare a custom error handler, the @errorhandler decorator is used. I'm going to put my
* Flask uses Python's logging package to write its logs, and this package already has the ability to send logs by email
* using SMTP debugging server - This fake email server accepts emails but instead of sending them it prints them to console
    `(venv) $ python -m smtpd -n -c DebuggingServer localhost:8025`
* To enable a file based log handler,  RotatingFileHandler needs to be attached to the application logger, in a similar way to the email handler.

#### 08.Followers
* Python includes a very useful `unittest` package that makes it easy to write and execute unit tests.

#### 09.Pagination
* Post/Redirect/Get (PRG) is a web development design pattern that allows for the page shown to the user after a form submission to be reloaded, shared or bookmarked without certain ill effects such as submitting the form another time.

* The paginate method can be called on any query object from Flask-SQLAlchemy. It takes three arguments: page number(starting from 1), no.of items per page, error flag

#### 10.Email
* Flask-Mail Usage
~~~py 
    $ flask shell
    >>> from flask_mail import Message
    >>> from app import mail
    >>> msg = Message('test subject', sender=app.config['ADMINS'][0],
    ... recipients=['your-email@example.com'])
    >>> msg.body = 'text body'
    >>> msg.html = '<h1>HTML body</h1>'
    >>> mail.send(msg)
~~~

* When working with threads there is an important design aspect of Flask that needs to be kept in mind. Flask uses contexts to avoid having to pass arguments across functions. I'm not going to go into a lot of detail on this, but know that there are two types of contexts, the `application context` and the `request context`. In most cases, these contexts are automatically managed by the framework, but when the application starts custom threads, contexts for those threads may need to be manually created.

#### 11.Facelift 
*  Flask-Bootstrap provides a ready to use base template that has the Bootstrap framework installed. With the extension initialized, a bootstrap/base.html template becomes available, and can be referenced from application templates with the extends clause.

#### 12.Dates and Times 

~~~py
from datetime import datetime
str(datetime.now())
str(datetime.utcnow())
~~~
* https://momentjs.com/



#### Miscellaneous
1. Werkzeug is a comprehensive WSGI(Web Server Gateway Interface) web application library.  Flask wraps Werkzeug, using it to handle the details of WSGI while providing more structure and patterns for defining powerful applications.


