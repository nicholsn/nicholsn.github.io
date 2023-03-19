AUTHOR = 'Nolan Nichols'
SITENAME = 'Nolan Nichols'
SITEURL = 'https://www.nolan-nichols.com'

# Static paths and cname mapping
PATH = "content"
STATIC_PATHS = ['images', 'extra/CNAME', 'extra/custom.css', 'extra/favicon.ico']
EXTRA_PATH_METADATA = {
    'extra/CNAME': {'path': 'CNAME'},
    'extra/custom.css': {'path': 'static/custom.css'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
}
PAGE_PATHS = ['pages']
ARTICLE_PATHS = ['articles']
ARTICLE_EXCLUDES = ['.']

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = 'en'

# Theme
THEME = "/Users/nnichols/Code/pelican-themes/elegant"

# Elegant theme settings.
TAGS_URL = "tags"
CATEGORIES_URL = "categories"
ARCHIVES_URL = "archives"
ARTICLE_URL = "{slug}"
PAGE_URL = "{slug}"
PAGE_SAVE_AS = "{slug}.html"
SEARCH_URL = "search"
LANDING_PAGE_TITLE = "Blog"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ((),)

# Social widget
SOCIAL = (("Gmail", "mailto:nolan.nichols@gmail.com"),
          ('Github', 'https://github.com/nicholsn'),
          ('LinkedIn', 'http://www.linkedin.com/in/nolannichols'),
          ("RSS", f"{SITEURL}/feeds/all.atom.xml"),)
SOCIAL_PROFILE_LABEL = u'Stay in Touch'

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

PLUGINS = ['webassets', 'tipue_search', 'liquid_tags']
LIQUID_TAGS = ["img", "literal", "video", "youtube",
               "vimeo", "include_code"]
