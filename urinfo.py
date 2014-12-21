# needed to extract HTML title
from bs4 import BeautifulSoup

# needed to perform remote HTTP HEAD request on URI
import requests

# create headers to pass when executing HTTP requests
USERAGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.34 (KHTML, like Gecko) Qt/4.8.3 Safari/534.34 urinfo"
HEADERS = {'User-Agent' : USERAGENT}

def urinfo( uri ):
    """
    Accept a uri and return info on success.
    Return a False on failure.
    TODO: do we want to return failure reasons?
    """

    try:
        result = requests.head(uri, headers=HEADERS, allow_redirects=True, timeout=4.0)
    except requests.ConnectionError:
        return False
    except requests.Timeout:
        return False

    if not result:
        return False

    info = {}
    info['uri'] = uri

    # copy headers into our return obj (except for cookies)
    # HACK the lowercasing is for the `responses` library which is used for mocking requests (testing only)
    info['headers'] = dict((k.lower(), v) for k,v in result.headers.iteritems())
    if 'set-cookie' in info['headers']:
        del info['headers']['set-cookie']

    if info['headers'].get('content-type') != None:
        if 'html' in info['headers']['content-type']:
            try:
                result = requests.get(uri, headers=HEADERS, allow_redirects=True, timeout=4.0)
            except requests.Timeout:
                return False

            soup = BeautifulSoup(result.content)
            if soup.title and soup.title.string:
                info['title'] = _sanitize_html_title(soup.title.string)

    return info

def _sanitize_html_title(title):
    """Accept an HTML title (string) and sanitize for output"""
    # replace all newlines with a space, encode all characters to ascii
    return title.replace('\n', ' ')

