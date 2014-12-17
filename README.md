# urinfo-api

Capture some basic information associated with a given URI

## Installation

Use the Heroku button below!

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

## Usage

```
curl http://localhost/fetch?uri=http://www.google.com
{
  "headers": {
    "alternate-protocol": "80:quic",
    "cache-control": "private, max-age=0",
    "content-encoding": "gzip",
    "content-length": "16402",
    "content-type": "text/html; charset=UTF-8",
    "date": "Sun, 23 Mar 2014 04:16:07 GMT",
    "expires": "-1",
    "p3p": "CP=\"This is not a P3P policy! See http://www.google.com/support/accounts/bin/answer.py?hl=en&answer=151657 for more info.\"",
    "server": "gws",
    "x-frame-options": "SAMEORIGIN",
    "x-xss-protection": "1; mode=block"
  },
  "title": "Google",
  "uri": "http://www.google.com"
}
```

## Tests

```
nosetests
```

