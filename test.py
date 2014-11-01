#!/usr/bin/env python

"""Tests for the Flask Heroku template."""

import unittest
from app import app
from urinfo import urinfo
from urinfo import _sanitize_html_title


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_home_page_dead(self):
        rv = self.app.get('/')
        self.assertTrue(rv.data)
        self.assertEqual(rv.status_code, 404)

    # we removed this page?
    #def test_about_page_works(self):
    #    rv = self.app.get('/about/')
    #    self.assertTrue(rv.data)
    #    self.assertEqual(rv.status_code, 200)

    # page /about missing so redirect to /about/ broke ...
    #def test_default_redirecting(self):
    #    rv = self.app.get('/about')
    #    self.assertEqual(rv.status_code, 301)

    def test_404_page(self):
        rv = self.app.get('/i-am-not-found/')
        self.assertEqual(rv.status_code, 404)

    def test_static_text_file_request(self):
        rv = self.app.get('/robots.txt')
        self.assertTrue(rv.data)
        self.assertEqual(rv.status_code, 200)
        rv.close()

    def test_fetch_success(self):
        rv = self.app.get('/fetch?uri=http://example.com')
        self.assertTrue(rv.data)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.mimetype, 'application/json')
        rv.close()

    def test_fetch_missing_uri(self):
        rv = self.app.get('/fetch')
        self.assertTrue(rv.data)
        self.assertEqual(rv.status_code, 404)
        rv.close()

    def test_fetch_failure(self):
        rv = self.app.get('/fetch?uri=http://this.uri.is.not.valid')
        self.assertTrue(rv.data)
        self.assertEqual(rv.status_code, 404)
        rv.close()

def test_urinfo_success():
    #{"uri": "http://example.com", "title": "Example Domain", "content-type": "text/html", "content-length": "1270"}
    uri = 'http://example.com'
    result = urinfo(uri)
    assert result['uri'] == uri
    assert result['title'] == 'Example Domain'

def test_urinfo_failure_is_false():
    uri = 'http://this.uri.is.not.valid'
    result = urinfo(uri)
    assert result == False

def test_sanitize_html_title_removes_newlines():
    title = 'this is a title\nwith \n a newline.'
    sanitize_title = _sanitize_html_title(title)
    assert title != sanitize_title
    assert '\n' not in sanitize_title

if __name__ == '__main__':
    unittest.main()
