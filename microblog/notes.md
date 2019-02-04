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
    - Instead of writing links directly, Flask provides a function called url_for(), which generates URLs using its internal mapping of URLs to view functions. 
    - The argument to url_for() is the endpoint name, which is the name of the view function.  For example, url_for('login') returns /login, and url_for('index') return '/index

#### ToDo: 

