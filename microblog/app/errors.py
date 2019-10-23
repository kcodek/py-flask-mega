from flask import render_template
from app import app, db

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404  # second value after the template is the error code

@app.errorhandler(500)
def internal_error(error):
    '''To make sure any failed db sessions do not interfere with any db accesses
    triggered by the template, the session is reset to a clean state.'''
    db.session.rollback()
    return render_template('500.html'), 500