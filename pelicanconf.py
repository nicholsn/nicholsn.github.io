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
SHOW_ARTICLE_AUTHOR = True
SHOW_ARTICLE_CATEGORY = True
USE_PAGER = True
BOOTSTRAP_FLUID = True
RELATED_POSTS_MAX = 10
USE_OPEN_GRAPH = True

# Notebook Rendering
NOTEBOOK_DIR = 'notebooks'
EXTRA_HEADER = open('_nb_header.html').read().decode('utf-8')

# Template settings
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False
DIRECT_TEMPLATES = ('index', 'categories', 'authors', 'archives', 'search')

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),)
TAG_CLOUD_MAX_ITEMS = 20
DISPLAY_TAGS_ON_SIDEBAR = True
DISPLAY_TAGS_INLINE = True
DISPLAY_CATEGORIES_ON_SIDEBAR = True 
HIDE_SIDEBAR = False

# Articles per page
DEFAULT_PAGINATION = 10
RECENT_POST_COUNT = 5

# Plugins
PLUGIN_PATHS = ["/Users/nolan/Repos/pelican-plugins"]
PLUGINS = ['related_posts', 'tipue_search', 'liquid_tags.img',
           'liquid_tags.video', 'liquid_tags.youtube',
           'liquid_tags.vimeo', 'liquid_tags.include_code',
           'liquid_tags.notebook']

# Static paths and cname mapping
PATH = "content"
STATIC_PATHS = ['images', 'extra/CNAME']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},}
PAGE_PATHS = ['pages']
ARTICLE_PATHS = ['articles']
ARTICLE_EXCLUDES = ['.']


# Social widget
SOCIAL = (('Github', 'https://github.com/nicholsn'),
          ('LinkedIn', 'http://www.linkedin.com/in/nolannichols'),)

# Disqus config
DISQUS_SITENAME = "nicholsn"

# Addthis
ADDTHIS_PROFILE = "ra-55f098e034ebcb96"
ADDTHIS_DATA_TRACK_ADDRESSBAR = False

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
