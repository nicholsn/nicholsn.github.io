#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import os

AUTHOR = "Nolan Nichols"
SITENAME = "Nolan Nichols"
#SITESUBTITLE = "musings of a neuroinformatician"
SITEURL = ""

TIMEZONE = "America/Vancouver"

DEFAULT_LANG = "en"

# Theme
THEME = "pelican-bootstrap3"

# Theme specific config
BOOTSTRAP_THEME = "slate"
PYGMENTS_STYLE = 'solarizeddark'
SITELOGO = ""
SITELOGO_SIZE = ""
HIDE_SITENAME = False
#DISPLAY_BREADCRUMBS = True
#DISPLAY_CATEGORY_IN_BREADCRUMBS = True
BOOTSTRAP_NAVBAR_INVERSE = False
FAVICON = "images/favicon.png"
DISPLAY_ARTICLE_INFO_ON_INDEX = True
ABOUT_ME = ""
AVATAR = "https://en.gravatar.com/userimage/26595965/475a270547e0d8313e94494e9a17f10f.png?size=200"
CC_LICENSE = "CC-BY"

# Template settings
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False
MENUITEMS = []

# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'),)
TAG_CLOUD_MAX_ITEMS = 20
DISPLAY_TAGS_ON_SIDEBAR = True
DISPLAY_TAGS_INLINE = True
DISPLAY_CATEGORIES_ON_SIDEBAR = True 
HIDE_SIDEBAR = False

# Articles per page
DEFAULT_PAGINATION = 10
RECENT_POST_COUNT = 5

# Plugins
PLUGIN_PATHS = "/Users/nolan/Repos/pelican-plugins"
PLUGINS = ["related_posts"]

# Static paths and cname mapping
STATIC_PATHS = ['images', 'extra/CNAME']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},}

# Social widget
SOCIAL = (('Github', 'https://github.com/nicholsn'),
          ('LinkedIn', 'http://www.linkedin.com/in/nolannichols'),)

# Disqus config
DISQUS_SITENAME = "nicholsn"
#DISQUS_SECRET_KEY = open(os.path.join(os.path.expanduser('~'), '.disqus_secret_key')).read()
#DISQUS_PUBLIC_KEY = u'iSFOPGc1Dvv6EmPU01BRQt1bK9GproBDnPc5IVFLJj7ETeEFMXVM5YiXwcTcK3Bd'

# Github
GITHUB_USER = "nicholsn"
GITHUB_REPO_COUNT = 3
GITHUB_SKIP_FORK = True
GITHUB_SHOW_USER_LINK = True
ARTICLE_EDIT_LINK = 'https://github.com/nicholsn/nicholsn.github.io/blob/gh-pages/content/%(slug)s.md'

# Google registration
GOOGLE_SEARCH = "001358792457409399469:hzfp1rcbkgw"
GOOGLE_ANALYTICS_UNIVERSAL = "UA-49888620-1"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = False
CATEGORY_FEED_ATOM = False
TRANSLATION_FEED_ATOM = None

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
