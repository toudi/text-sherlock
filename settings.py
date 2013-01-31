# -*- coding: utf-8 -*-
"""
Created by Christopher Bess (https://github.com/cbess/text-sherlock)
Copyright 2013 
"""
import os
from app_args import get_options
config = {}
try:
    import yaml
    # Try to load local settings, which override the default settings.
    # In local_settings.yml, set the values for any settings you want to override.
    default_yaml_path = os.path.join(os.path.dirname(__file__), 'local_settings.yml')
    yaml_path = get_options().config
    if os.path.isfile(default_yaml_path):
        yaml_path = default_yaml_path
        # try default path, proj/root directory
        config = yaml.load(open(yaml_path, 'r'))
    elif yaml_path and os.path.isfile(yaml_path):
        # try the specified config path
        config = yaml.load(open(yaml_path, 'r'))
    if config:
        print 'Loaded Sherlock config from %s' % yaml_path
except ImportError:
    print 'No yaml lib: pip install pyyaml'
    
# `%(sherlock_dir)s` resolves to the directory where sherlock is installed.

# A value indicating whether the app runs in debug mode.
# type: boolean
# default: True (set to False for production or in untrusted environments)
DEBUG = config.get('debug', True)

# Should not be changed, this is the absolute path to the directory
# containing main.py, settings.py, core/, etc.
# type: string
# default: os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(__file__)

# An absolute path to the directory that will store all indexes
# for the search engine. Must have trailing slash.
# type: string
# default: '%(sherlock_dir)s/data/indexes/'
INDEXES_PATH = config.get('indexes_path', '%(sherlock_dir)s/data/indexes/')

# True if the target path will be indexed recursively (includes sub directories).
# type: boolean
# default: True
INDEX_RECURSIVE = config.get('index_recursive', True)

# An absolute path to the directory path that will store the logs.
# Set to an empty string to disable logging.
# type: string
# default: ''
LOG_PATH = config.get('log_path', '')

# New line character value, may be '\n' or '\r\n'.
# type: character|string
# default: '\n'
NEW_LINE = config.get('new_line', '\n')

# During the indexing all items with the given suffix will be exclude from the
# index. Only checks filenames, for now.
# type: tuple
# default: None
EXCLUDE_FILE_SUFFIX = config.get('exclude_file_suffix')

# The opposite of EXCLUDE_FILE_SUFFIX. This **only** includes files that match
# a given suffix.
# type: tuple
# default: None
INCLUDE_FILE_SUFFIX = config.get('include_file_suffix')

# Number of lines used when displaying the results
# context per hit. This needs to be one (1) or greater.
# type: integer
# default: 1
NUM_CONTEXT_LINES = config.get('num_context_lines', 1)

# The absolute path to index when the indexing is performed.
# This is the index that has the original text to be indexed. This is also used
# when displaying the actual document from the search results. Must have
# trailing slash. The user running the app must have read access to the path.
# type: string
# default: '%(sherlock_dir)s/tests/text/'
INDEX_PATH = config.get('index_path', '%(sherlock_dir)s/tests/text/')

# The default index name that is used for an index created within INDEXES_PATH.
# type: string
# default: 'main'
DEFAULT_INDEX_NAME = config.get('default_index_name', 'main')

# The name of the server type to use as the web server.
# CherryPy support is built-in, if production: 'cherrypy'.
# type: string
# default: None
SERVER_TYPE = config.get('server_type')

# The local port to expose the web server.
# type: integer
# default: 7777
SERVER_PORT = config.get('server_port', 7777)

# The local address to access the web server (the host name to listen on).
# Use '0.0.0.0' to make it available externally.
# type: string
# default: '127.0.0.1' or 'localhost'
SERVER_ADDRESS = config.get('SERVER_ADDRESS', '127.0.0.1')

# Default number of results per page.
# type: integer
# default: 10
RESULTS_PER_PAGE = config.get('results_per_page', 10)

# Default number of sub results shown in each search result.
# type: integer
# default: 3
MAX_SUB_RESULTS = config.get('max_sub_results', 3)

# Default file indexer and searcher. Available indexers: whoosh and xapian
# They can be set to different values only if the two backends are compatible
# with each other.
# type: string
# default: 'whoosh'
DEFAULT_SEARCHER = DEFAULT_INDEXER = config.get('default_indexer', 'whoosh')

# Default indexing backend.
# This must be full import name.
# type: string
# default: 'core.sherlock.backends.whoosh_backend.WhooshIndexer'
INDEXING_BACKEND = config.get('indexing_backend', 'core.sherlock.backends.whoosh_backend.WhooshIndexer')

# Allows the indexer to ignore errors produced during file indexing.
# For example: any unicode or file read errors, it will skip indexing those files.
# Backends are not required to support this setting.
# Built-in backends (whoosh and xapian) honor this setting.
# default: not Debug (opposite of Debug value) = False
IGNORE_INDEXER_ERRORS = not DEBUG

# The tag used to wrap the matched term in the search results. The first index
# is placed in the front of the matched term and the second index goes after
# the matched term.
# type: tuple
# default: ("<span class='match'>", "</span>")
MATCHED_TERM_WRAP = config.get('matched_term_wrap', ("<span class='match'>", "</span>"))

# The banner text displayed in the header of each page.
# type: string/html
# default: 'Sherlock Search'
SITE_BANNER_TEXT = config.get('site_banner_text', 'Sherlock Search')

# The site title text (displayed in browser tab or title bar of window).
# This is appended to each auto-generated page title.
# type: string
# default: 'Text Sherlock'
SITE_TITLE = config.get('site_title', 'Text Sherlock')

# The site banner background color.
# This banner is shown at the top of each page.
# Possible values: black, blue, skyblue, silver, orange, white
# More colors can be added to 'bg-gradients.css'
# The banner text styles must be changed in the stylesheet:
#   main.css (#top-banner #banner-text)
# type: string
# default: black
SITE_BANNER_COLOR = config.get('site_banner_color', 'black')

# Projects to index
# This is a key-value dict, where:
# - the key is the name of the project. It will be displayed at the left menu.
# - the value keeps the configuration for this particular project. It's a key-value dict.
#   Avaliable keys:
#   - SOURCE
#            This is the 'source' of files to index. Possible values:
#            - core.sherlock.indexer.source.filesystem.FileSystem (if you plan to index directory from disk)
#            - core.sherlock.indexer.source.git.Git (if you plan to index git repository)
#   - SETTINGS
#            kwargs that will be passed to the source engine.
#            Possible values depend on the source class.
#            - Filesystem
#              - path: path to index
#              - recursive: whether to traverse inside subdirectories
#            - Git
#              - url: url to your git repo
#              - branch: branch to index (default: master)
#   - BACKEND
#            [ Optional ] backend to use. If none, use INDEXING_BACKEND
#   - INCLUDE_FILE_SUFFIX
#            per-project setting of INCLUDE_FILE_SUFFIX
#   - EXCLUDE_FILE_SUFFIX
#            per-project setting of EXCLUDE_FILE_SUFFIX

# Example local_settings.yml:
# ---
# projects:
#   TestProject:
#     exclude_file_suffix: [m, h]
#     settings: {path: '%(sherlock_dir)s/tests/text', recursive: true}
#     source: core.sherlock.indexer.source.filesystem.FileSystem

PROJECTS = config.get('projects', {})


# Use the local_settings.yml instead, noted at the top of file
try:
    from local_settings import *
    print '!!!Deprecated local_settings.py|pyc file found: Use local_settings.yml instead.'
except ImportError:
    pass
