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
from hurry.filesize import size

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')

USERAGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.34 (KHTML, like Gecko) Qt/4.8.3 Safari/534.34 https://bitbucket.org/russellballestrini/foxbot"
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

    if not url:
        abort(404)

    return json.dumps(urinfo(url))


###
# Application logic
###

def urinfo( msg ):
    info = {}
    words = msg.split()
    for word in words:
        if '://' in word:
            result = requests.head( word, headers=HEADERS, allow_redirects=True, timeout=4.0 )

            if not result:
                continue

            info['content-type'] = result.headers.get('content-type')
            if info['content-type']:
                info['url'] = word
                if 'html' in result.headers['content-type']:
                    result = requests.get( word )
                    soup = BeautifulSoup( result.content )
                    if soup.title: # if there is a title, append it to output 
                        info['title'] = soup.title.string.replace( '\n', ' ' ).encode('ascii', 'replace')

                try:
                    info['content-length'] = int(result.headers.get('content-length'))
                except:
                    pass
            return info
    return False


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
    messages = [
      'check out: https://linkpeek.com for webpage screenshots',
      'http://russell.ballestrini.net for a good read',
      'http://www.skills-1st.co.uk/papers/jane/ukuug_march09_zenoss.pdf',
      'erbody dance http://www.youtube.com/watch?v=12VUjgYMm1U',
      'OUCH! http://russell.ballestrini.net/wp-content/uploads/2012/06/dedication-eye-chemical-burn.jpg',
      'a http://www.barackobama.com/ asdf',
      'http://words.gumyum.com/',
    ]

    for message in messages:
        print urinfo( message )

    app.run(debug=True)


