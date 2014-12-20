#!/usr/bin/env python

import unittest
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
        # TODO mock this
        rv = self.app.get('/fetch?uri=http://example.com')
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

    def test_urinfo_success(self):
        """Test fetching a url"""
        #{"uri": "http://example.com", "title": "Example Domain", "content-type": "text/html", "content-length": "1270"}
        uri = 'http://example.com'
        result = urinfo(uri)
        assert result['uri'] == uri
        assert result['title'] == 'Example Domain'

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

if __name__ == '__main__':
    unittest.main()
