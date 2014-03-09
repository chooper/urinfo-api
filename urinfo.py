# needed to extract HTML title
from bs4 import BeautifulSoup

# needed to perform remote HTTP HEAD request on URI
import requests

# create headers to pass when executing HTTP  requests
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

    if not result:
        #return result
        return False

    info = {}
    info['uri'] = uri
    info['content-type'] = result.headers.get('content-type', None)
    info['content-length'] = result.headers.get('content-length', None)

    if info['content-type'] != None:
        if 'html' in info['content-type']:
            result = requests.get(uri, headers=HEADERS, allow_redirects=True, timeout=4.0)
            soup = BeautifulSoup(result.content)
            if soup.title:
                # replace all newlines with a space, encode all characters to ascii
                info['title'] = soup.title.string.replace('\n', ' ').encode('ascii', 'replace')

    return info
