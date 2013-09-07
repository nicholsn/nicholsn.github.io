#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Nolan Nichols'
SITENAME = u'Nolan-Nichols'
SITEURL = ''

TIMEZONE = 'America/Vancouver'

DEFAULT_LANG = u'en'

THEME = "niu-x2"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'),
          ('Python.org', 'http://python.org/'),
          ('Jinja2', 'http://jinja.pocoo.org/'),
          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

NIUX2_HEADER_SECTIONS = [ 
     ("About", "about", "/pages/about.html", "icon-book"),
     ("Research", "research", "/pages/research.html", "icon-beaker"),
     ("Archives", "archives", "/archives.html", "icon-archive"),
     ("Tags", "tags", "/tags.html", "icon-tag"),
]