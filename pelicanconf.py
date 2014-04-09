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

THEME = "pelican-bootstrap3"

PLUGIN_PATH = "/Users/nolan/PycharmProjects/pelican-plugins"
PLUGINS = ["neighbors", "related_posts", "disqus_static"]

STATIC_PATHS = ['images', 'extra/CNAME']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = False
CATEGORY_FEED_ATOM = False
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'))

# Social widget
SOCIAL = (('Github', 'https://github.com/nicholsn'),
          ('LinkedIn', 'http://www.linkedin.com/in/nolannichols'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# Menu Items
MENUITEMS = []

# Disqus config
DISQUS_SITENAME = "nicholsn"
DISQUS_SECRET_KEY = open(os.path.join(os.path.expanduser('~'), '.disqus_secret_key')).read()
DISQUS_PUBLIC_KEY = u'iSFOPGc1Dvv6EmPU01BRQt1bK9GproBDnPc5IVFLJj7ETeEFMXVM5YiXwcTcK3Bd'

ARTICLE_EDIT_LINK = 'https://github.com/nicholsn/nicholsn.github.io/blob/gh-pages/content/%(slug)s.md'


GOOGLE_SEARCH = "001358792457409399469:hzfp1rcbkgw"