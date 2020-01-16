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

#### 02. Templates
* Creating mock objects is a useful technique that allows you to concentrate on one part of the application without having to worry about other parts of the system that don't exist yet. 
    -   user = {'username': 'Miguel'}
* jinja2
* render_template
* {{}}, {% %}  - dynamic content, loops, conditionals
* template inheritance - {% extends ... %} {% block content %}{% endblock %}

#### 03. Web Forms
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



#### 04. Database
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

#### 05. User Logins
*  Flask-Login provides a mixin class called UserMixin that includes generic implementation of four required items -  is_authenticated, is_active , is_anonymous, get_id()

* Flask-Login keeps track of the logged in user by storing its unique identifier in Flask's user session, a storage space assigned to each user who connects to the application.

* The user loader is registered with Flask-Login with the `@login.user_loader` decorator. 

* The way Flask-Login protects a view function against anonymous users is with a decorator called `@login_required`.
* It is a standard practice to respond to a POST request generated by a web form submission with a redirect
* The current_user variable comes from Flask-Login and can be used at any time during the handling to obtain the user object that represents the client of the req
* login_user will register the user as logged in, so that means that any future pages the user navigates to will have the current_user variable set to that user.
* If the user navigates to /index, for example, the @login_required decorator will intercept the request and respond with a redirect to /login but it will add a query string argument to this URL, making the complete redirect URL /login?next=/index. The next query string argument is set to the original URL, so the application can use that to redirect back after login.

#### 06. Profile page & avatars
* The `@before_request` decorator from Flask register the decorated function to be executed right before the view function.

#### 07. Error Handling
* To run in debug mode - `$ export FLASK_DEBUG=1`. reloader is enabled in debug mode
* To declare a custom error handler, the @errorhandler decorator is used. I'm going to put my
* Flask uses Python's logging package to write its logs, and this package already has the ability to send logs by email
* using SMTP debugging server - This fake email server accepts emails but instead of sending them it prints them to console
    `(venv) $ python -m smtpd -n -c DebuggingServer localhost:8025`
* To enable a file based log handler,  RotatingFileHandler needs to be attached to the application logger, in a similar way to the email handler.

#### 08. Followers
* Python includes a very useful `unittest` package that makes it easy to write and execute unit tests.

#### 09. Pagination
* Post/Redirect/Get (PRG) is a web development design pattern that allows for the page shown to the user after a form submission to be reloaded, shared or bookmarked without certain ill effects such as submitting the form another time.

* The paginate method can be called on any query object from Flask-SQLAlchemy. It takes three arguments: page number(starting from 1), no.of items per page, error flag

#### 10. Email
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

#### 11. Facelift 
*  Flask-Bootstrap provides a ready to use base template that has the Bootstrap framework installed. With the extension initialized, a bootstrap/base.html template becomes available, and can be referenced from application templates with the extends clause.

#### 12. Dates and Times 

~~~py
from datetime import datetime
str(datetime.now())
str(datetime.utcnow())
~~~
* https://momentjs.com/

#### 13. I18n and L10n
* The Babel instance provides a localeselector decorator. The decorated function is invoked for each request to select a language translation to use for that request
* Once you have the application with all the _() and _l() in place, you can use the `pybabel` command to extract them to a .pot file, which stands for portable object template. This is a text file that includes all the texts that were marked as needing translation. The purpose of this file is to serve as a template to create translation files for each language.
* extract all text to .pot file - `(venv) $ pybabel extract -F babel.cfg -k _l -o messages.pot .`
* create a translation for each language that will be supported in addition to the base one,
    `(venv) $ pybabel init -i messages.pot -d app/translations -l es`
     creating catalog app/translations/es/LC_MESSAGES/messages.po based on messages.pot
* To use the translated texts, the file needs to be compiled -
   `(venv) $ pybabel compile -d app/translations`
    compiling catalog app/translations/es/LC_MESSAGES/messages.po to
    app/translations/es/LC_MESSAGES/messages.mo
* updating the translations
    `(venv) $ pybabel extract -F babel.cfg -k _l -o messages.pot .`
    `(venv) $ pybabel update -i messages.pot -d app/translations`
* Flask-Babel returns the selected language and locale for a given request via the get_locale() function, 

* Command-Line Enhancements
    - `flask run`, `flask shell`, and several `flask db` sub-commands provided by the Flask-Migrate extension. It is actually easy to add application-specific commands to flask as well.
    - This command uses the `@click.argument` decorator to define the language code. Click passes the value provided in the command to the handler function as an argument & this arg is incorporated in the command `init`
    `flask translate --help`, `flask translate init es`, `flask translate update`, `flask translate compile`

#### 14. AJAX
* In a strict client-side application the entire application is downloaded to the client with the initial page request, and then the application runs entirely on the client, only contacting the server to retrieve or store data and making dynamic changes to the appearance of that first and only web page. This type of applications are called Single Page Applications or SPAs.
* language translation -  `pip install guess_language-spirit`

* using a third-party translation service 
    - The two major translation services are Google Cloud Translation API and Microsoft Translator Text API. Both are paid services, but the Microsoft offering has an entry level option for low volume of translations that is free(needs an azure account). Google offered a free translation service in the past but today, even the lowest service tier is paid.

#### 15. A better application structure
* The blueprints feature of Flask helps achieve a more practical organization that makes it easier to reuse code.
* A better solution would be to not use a global variable for the application, and instead use an application factory function to create the function at runtime. 
* This would be a function that accepts a configuration object as an argument, and returns a Flask application instance, configured with those settings.
* In Flask, a `blueprint` is a logical structure that represents a subset of the application. A blueprint can include elements such as routes, view functions, forms, templates and static files. If you write your blueprint in a separate Python package, then you have a component that encapsulates the elements related to specific feature of the application.
* The contents of a blueprint are initially in a dormant state. To associate these elements, the blueprint needs to be registered with the application. During the registration, all the elements that were added to the blueprint are passed on to the application. So you can think of a blueprint as a temporary storage for application functionality that helps in organizing your code.

* The creation of a blueprint is fairly similar to the creation of an application. This is done in the ___init__.py module of the blueprint package


* BluePrints
    - Error Handling Blueprint - encapsulates the support for error handlers.  
    - Authentication Blueprint - The register_blueprint() call in this case has an extra argument, url_prefix. This is entirely optional, but Flask gives you the option to attach a blueprint under a URL prefix, so any routes defined in the blueprint get this prefix in their URLs. In many cases this is useful as a sort of "namespacing" that keeps all the routes in the blueprint separated from other routes in the application or other blueprints
    - Main Applicationi Blueprint

* The Application Factory Pattern
    - create_app() that constructs a Flask application instance, and eliminate the global variable.     

* The `current_app` variable that Flask provides is a special "context" variable that Flask initializes with the application before it dispatches a request. You have already seen another context variable before, the `g` variable in which I'm storing the current locale. These two, along with Flask-Login's `current_user` and a few others you haven't seen yet, are somewhat "magical" variables, in that they work like global variables, but are only accessible during the handling of a request, and only in the thread that is handling it.

* tests 
    - Before invoking your view functions, Flask pushes an application context, which brings `current_app` and `g` to life. When the request is complete, the context is removed, along with these variables. For the db.create_all() call to work in the unit testing setUp() method, Push an application context for the application instance created, and in that way, db.create_all() can use current_app.config to know where is the database. Then in the tearDown() method pop the context to reset everything to a clean state.

* The `application context` is one of two contexts that Flask uses. There is also a `request context`, which is more specific, as it applies to a request. When a request context is activated right before a request is handled, Flask's request and session variables become available, as well as Flask-Login's current_user.

* .env file
    - The .env file can be used for all the configuration-time variables, but it cannot be used for Flask's FLASK_APP and FLASK_DEBUG environment variables, because these are needed very early in the application bootstrap process, before the application instance and its configuration object exist.

#### 16. Full-Text Search
* Elasticsearch is a full-text search engine. Data in Elasticsearch is written to indexes. Unlike a relational database, the data is just a JSON object.
* 


#### 19. Deployment on Docker Containers

> docker commands  
`$ docker build -t microblog:latest .`  
`$ docker run --name microblog -d -p 8000:5000 --rm microblog:latest`  
`$ docker container stop microblog`  
- with runtime environment variables
>  $ docker run --name microblog -d -p 8000:5000 --rm -e SECRET_KEY=my-secret-key \
    -e MAIL_SERVER=smtp.googlemail.com -e MAIL_PORT=587 -e MAIL_USE_TLS=true \
    -e MAIL_USERNAME=<your-gmail-username> -e MAIL_PASSWORD=<your-gmail-password> \
    microblog:latest

> $ docker run --name mysql -d -e MYSQL_RANDOM_ROOT_PASSWORD=yes \
    -e MYSQL_DATABASE=microblog -e MYSQL_USER=microblog \
    -e MYSQL_PASSWORD=<database-password> \
    mysql/mysql-server:5.7

> $ docker run --name elasticsearch -d -p 9200:9200 -p 9300:9300 --rm \
    -e "discovery.type=single-node" \
    docker.elastic.co/elasticsearch/elasticsearch-oss:6.1.1    

>  $ docker run --name microblog -d -p 8000:5000 --rm -e SECRET_KEY=my-secret-key \
    -e MAIL_SERVER=smtp.googlemail.com -e MAIL_PORT=587 -e MAIL_USE_TLS=true \
    -e MAIL_USERNAME=<your-gmail-username> -e MAIL_PASSWORD=<your-gmail-password> \
    --link mysql:dbserver \
    -e DATABASE_URL=mysql+pymysql://microblog:<database-password>@dbserver/microblog \
    --link elasticsearch:elasticsearch \
    -e ELASTICSEARCH_URL=http://elasticsearch:9200 \
    microblog:latest

    





#### Miscellaneous
1. Werkzeug is a comprehensive WSGI(Web Server Gateway Interface) web application library.  Flask wraps Werkzeug, using it to handle the details of WSGI while providing more structure and patterns for defining powerful applications.

