#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Nolan Nichols'
SITENAME = u'Nolan Nichols'
SITESUBTITLE= "ramblings of a neuroinformatician"
SITEURL = 'http://nicholsn.github.io'

TIMEZONE = 'America/Vancouver'

DEFAULT_LANG = u'en'

THEME = "plumage"

PLUGIN_PATH = "/Users/nolan/PycharmProjects/pelican-plugins"
PLUGINS = ["neighbors", "related_posts", ]

SITE_THUMBNAIL = "https://en.gravatar.com/userimage/26595965/475a270547e0d8313e94494e9a17f10f.png"
SITE_THUMBNAIL_TEXT = "Nolan Nichols"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'),
          ('Python.org', 'http://python.org/'),
          ('Jinja2', 'http://jinja.pocoo.org/'),
         )

# Social widget
SOCIAL = (('Github', 'https://github.com/nicholsn'),
          ('LinkedIn', 'http://www.linkedin.com/in/nolannichols'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# Menu Items
MENUITEMS = []

DISQUS_SITENAME = "nolan-nichols"

GOOGLE_SEARCH = "001358792457409399469:hzfp1rcbkgw"