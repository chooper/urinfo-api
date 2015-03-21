#!/usr/bin/env python

import unittest
import responses
import requests
from app import app
from urinfo import urinfo
from urinfo import _sanitize_html_title

# One minor note about the `responses` lib... it apparently requires
# a trailing '/' on hostnames or it will throw requests.ConnectionError

class TestWebApp(unittest.TestCase):
    """Test the web app"""

    def setUp(self):
        self.app = app.test_client()

    def test_home_page_dead(self):
        """Test that root returns a 404"""
        rv = self.app.get('/')
        self.assertTrue(rv.data)
        self.assertEqual(rv.status_code, 404)

    def test_404_page(self):
        """Test that an obviously bad url returns a 404"""
        rv = self.app.get('/i-am-not-found/')
        self.assertEqual(rv.status_code, 404)

    def test_robots_txt_file_request(self):
        """Test that robots.txt returns successfully"""
        rv = self.app.get('/robots.txt')
        self.assertTrue(rv.data)
        self.assertEqual(rv.status_code, 200)
        rv.close()

    @responses.activate
    def test_fetch_success(self):
        """Test /fetch returns a correct response for a successful URL"""
        uri = 'http://255.255.255.255/'

        def head_callback(req):
            body = 'something'
            headers = {'content-type': 'text/html'}
            return (200, headers, body)

        def get_callback(req):
            body = '<!doctype html><html><head><title>Test Title</title></head></html>'
            headers = {'content-type': 'text/html'}
            return (200, headers, body)

        responses.add_callback(responses.HEAD, uri, callback=head_callback, content_type='text/html')
        responses.add_callback(responses.GET,  uri, callback=get_callback,  content_type='text/html')

        rv = self.app.get('/fetch?uri={0}'.format(uri))
        self.assertTrue(rv.data)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.mimetype, 'application/json')
        rv.close()

    def test_fetch_missing_uri(self):
        """Test /fetch returns a 404 when not given a uri"""
        rv = self.app.get('/fetch')
        self.assertTrue(rv.data)
        self.assertEqual(rv.status_code, 404)
        rv.close()

    @responses.activate
    def test_fetch_failure(self):
        """Test /fetch returns a 404 for an invalid uri"""
        uri = 'http://255.255.255.255/'
        responses.add(responses.GET, uri, body=requests.ConnectionError())

        rv = self.app.get('/fetch?uri={0}'.format(uri))
        self.assertTrue(rv.data)
        self.assertEqual(rv.status_code, 404)
        rv.close()


class TestUrinfo(unittest.TestCase):
    """Test the urinfo library"""

    def test_sanitize_html_title_removes_newlines(self):
        """Test that we strip newlines from titles"""
        title = 'this is a title\nwith \n a newline.'
        sanitize_title = _sanitize_html_title(title)
        self.assertTrue(title != sanitize_title)
        self.assertTrue('\n' not in sanitize_title)

    def test_sanitize_html_title_removes_repetitive_whitespace(self):
        """Test that we remove repetitive whitespace"""
        title = 'this is a title        with extra whitespace.'
        sanitize_title = _sanitize_html_title(title)
        self.assertTrue(title != sanitize_title)
        self.assertTrue('  ' not in sanitize_title)
        self.assertTrue(' ' in sanitize_title)

    @responses.activate
    def test_urinfo_success(self):
        """Test fetching a url on the happy path"""

        uri = 'http://255.255.255.255/'

        def head_callback(req):
            body = 'something'
            headers = {'content-type': 'text/html'}
            return (200, headers, body)

        def get_callback(req):
            body = '<!doctype html><html><head><title>Test Title</title></head></html>'
            headers = {'content-type': 'text/html'}
            return (200, headers, body)

        responses.add_callback(responses.HEAD, uri, callback=head_callback, content_type='text/html')
        responses.add_callback(responses.GET,  uri, callback=get_callback,  content_type='text/html')

        result = urinfo(uri)
        self.assertEqual(result['uri'], uri)
        self.assertEqual(result['title'], 'Test Title')

    @responses.activate
    def test_urinfo_connection_error_get(self):
        """Test that a connection error during urinfo returns False"""
        uri = 'http://255.255.255.255/'

        # test error during GET
        responses.add(responses.GET, uri, body=requests.ConnectionError())
        result = urinfo(uri)
        self.assertEqual(result, False)

    @responses.activate
    def test_urinfo_connection_error_head(self):
        """Test that a connection error during urinfo returns False"""
        uri = 'http://255.255.255.255/'

        # test error during HEAD
        responses.add(responses.HEAD, uri, body=requests.ConnectionError())
        result = urinfo(uri)
        self.assertEqual(result, False)

    @responses.activate
    def test_urinfo_timeout_get(self):
        """Test that a timeout error during urinfo returns False"""
        uri = 'http://255.255.255.255/'

        # test error during GET
        responses.add(responses.GET, uri, body=requests.Timeout())
        result = urinfo(uri)
        self.assertEqual(result, False)

    @responses.activate
    def test_urinfo_timeout_head(self):
        """Test that a timeout error during urinfo returns False"""
        uri = 'http://255.255.255.255/'

        # test error during HEAD
        responses.add(responses.HEAD, uri, body=requests.Timeout())
        result = urinfo(uri)
        self.assertEqual(result, False)

    @responses.activate
    def test_urinfo_http_error_get(self):
        """Test that a http error during urinfo returns False"""
        uri = 'http://255.255.255.255/'

        # test error during GET
        responses.add(responses.GET, uri, body=requests.HTTPError())
        result = urinfo(uri)
        self.assertEqual(result, False)

    @responses.activate
    def test_urinfo_http_error_head(self):
        """Test that a http error during urinfo returns False"""
        uri = 'http://255.255.255.255/'

        # test error during HEAD
        responses.add(responses.HEAD, uri, body=requests.HTTPError())
        result = urinfo(uri)
        self.assertEqual(result, False)


if __name__ == '__main__':
    unittest.main()
