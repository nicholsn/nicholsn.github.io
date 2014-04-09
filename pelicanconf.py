#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import os

AUTHOR = u'Nolan Nichols'
SITENAME = u'Nolan Nichols'
#SITESUBTITLE = "musings of a neuroinformatician"
SITEURL = ''

TIMEZONE = 'America/Vancouver'

DEFAULT_LANG = u'en'

# Theme config
THEME = "pelican-bootstrap3"

# Template settings
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = True
MENUITEMS = []

# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'))

# Plugins
PLUGIN_PATH = "/Users/nolan/PycharmProjects/pelican-plugins"
PLUGINS = ["neighbors", "related_posts", "disqus_static"]

# Static paths and cname mapping
STATIC_PATHS = ['images', 'extra/CNAME']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},}

# Social widget
SOCIAL = (('Github', 'https://github.com/nicholsn'),
          ('LinkedIn', 'http://www.linkedin.com/in/nolannichols'),)

# Articles per page
DEFAULT_PAGINATION = 10

# Disqus config
DISQUS_SITENAME = "nicholsn"
DISQUS_SECRET_KEY = open(os.path.join(os.path.expanduser('~'), '.disqus_secret_key')).read()
DISQUS_PUBLIC_KEY = u'iSFOPGc1Dvv6EmPU01BRQt1bK9GproBDnPc5IVFLJj7ETeEFMXVM5YiXwcTcK3Bd'

# Edit on Github
ARTICLE_EDIT_LINK = 'https://github.com/nicholsn/nicholsn.github.io/blob/gh-pages/content/%(slug)s.md'

# Google registration
GOOGLE_SEARCH = "001358792457409399469:hzfp1rcbkgw"

# Analytics
GOOGLE_ANALYTICS_UNIVERSAL = "UA-49888620-1"
GOOGLE_ANALYTICS_UNIVERSAL_PROPERTY = ""

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = False
CATEGORY_FEED_ATOM = False
TRANSLATION_FEED_ATOM = None

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True