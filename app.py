"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os
from flask import Flask, render_template, request, redirect, url_for, abort
import json
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')

USERAGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.34 (KHTML, like Gecko) Qt/4.8.3 Safari/534.34 urinfo"
HEADERS = { 'User-Agent' : USERAGENT }


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/fetch')
def fetch():
    url = request.args.get('url')

    # abort with 404 if url missing from query params
    if url == None:
        abort(404)

    # get urinfo
    info = urinfo(url)

    # if info is False or None, abort with 404
    if info == None or info == False:
        abort(404)

    return json.dumps(info)


###
# Application logic
###

def urinfo( url ):
    """
    Accept a uri and return info on HEAD request success.
    Return False on HEAD request failure.
    Return None if HEAD request is not True.
    """

    try:
        result = requests.head( url, headers=HEADERS, allow_redirects=True, timeout=4.0 )
    except requests.ConnectionError:
        return False

    if not result:
        return result

    info = {}
    info['url'] = url
    info['content-type'] = result.headers.get('content-type')
    info['content-length'] = result.headers.get('content-length')

    # content-type could be NoneType which is not iterable.
    if 'html' in (info['content-type'] or ''):
        result = requests.get( url )
        soup = BeautifulSoup( result.content )
        if soup.title:
            info['title'] = soup.title.string.replace( '\n', ' ' ).encode('ascii', 'replace')

    return info


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
    return render_template('404.html'), 404


if __name__ == '__main__':

    app.run(debug=True)

