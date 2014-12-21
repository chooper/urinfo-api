#!/usr/bin/env python

import unittest
import responses
from app import app
from urinfo import urinfo
from urinfo import _sanitize_html_title


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

    def test_fetch_success(self):
        """Test /fetch returns a correct response for example.com"""
        uri = 'http://example.com'
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

    def test_fetch_failure(self):
        """Test /fetch returns a 404 for an invalid uri"""
        rv = self.app.get('/fetch?uri=http://this.uri.is.not.valid')
        self.assertTrue(rv.data)
        self.assertEqual(rv.status_code, 404)
        rv.close()


class TestUrinfo(unittest.TestCase):
    """Test the urinfo library"""

    def test_urinfo_failure_is_false(self):
        """Test that DNS resolution or connection failures return False"""
        uri = 'http://this.uri.is.not.valid'
        result = urinfo(uri)
        assert result == False

    def test_sanitize_html_title_removes_newlines(self):
        """Test that we strip newlines from titles"""
        title = 'this is a title\nwith \n a newline.'
        sanitize_title = _sanitize_html_title(title)
        assert title != sanitize_title
        assert '\n' not in sanitize_title

    @responses.activate
    def test_urinfo_success(self):
        """Test fetching a url"""

        uri = 'http://255.255.255.255/'

        def head_callback(req):
            body = 'something'
            headers = {'content-type': 'text/html'}
            return (200, headers, body)

        def get_callback(req):
            body = '<!doctype html><html><head><title>Example Domain</title></head></html>'
            headers = {'content-type': 'text/html'}
            return (200, headers, body)

        responses.add_callback(responses.HEAD, uri, callback=head_callback, content_type='text/html')
        responses.add_callback(responses.GET,  uri, callback=get_callback,  content_type='text/html')
        result = urinfo(uri)
        self.assertEqual(result['uri'], uri)
        self.assertEqual(result['title'], 'Example Domain')

if __name__ == '__main__':
    unittest.main()
