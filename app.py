"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os

from flask import Flask
from flask import jsonify
from flask import render_template, request, redirect, url_for, abort, got_request_exception
import rollbar
import rollbar.contrib.flask
from urinfo import urinfo

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')

if os.environ.get('DEBUG', 0) > 1:
    app.debug = True

rollbar_access_key = os.environ.get('ROLLBAR_ACCESS_KEY')
if rollbar_access_key:
    rollbar.init(
        rollbar_access_key,
        'urinfo',
        root=os.path.dirname(os.path.realpath(__file__)),
        allow_logging_basic_config=False
    )

    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/fetch')
def fetch():
    uri = request.args.get('uri')

    # abort with 404 if uri missing from query params
    if uri == None:
        abort(404)

    # abort with 404 if uri is not a HTTP(s) uri
    if not uri.lower().startswith("http"):
        abort(404)

    # get urinfo
    info = urinfo(uri)

    # if info is False or None, abort with 404
    if info == None or info == False:
        abort(404)

    return jsonify(**info)


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return 'null', 404


if __name__ == '__main__':

    app.run(debug=True)

