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





#### ToDo: 

