#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
main.py - Runs the main application.

Created by Christopher Bess (https://github.com/cbess/text-sherlock)
Copyright 2012
"""

from app_args import get_options, get_app_args
from webapp import server
from core.sherlock import indexer, backends, db
from core import get_version_info
import settings
import sys


def show_version():
    pyver = sys.version_info
    print '  Python: v%d.%d.%d' % (pyver[0], pyver[1], pyver[2])
    print 'Sherlock: v' + get_version_info('sherlock')
    print '   Flask: v' + get_version_info('flask')
    print '  Whoosh: v' + get_version_info('whoosh')
    print 'CherryPy: v' + get_version_info('cherrypy')
    

def show_stats():
    # backend stats
    print 'Available indexer backends: %s' % backends.indexer_names()
    print 'Available searcher backends: %s' % backends.searcher_names()
    print 'Current backend: %s' % settings.DEFAULT_SEARCHER
    # indexer stats
    idx = indexer.Indexer()
    print(
        'Total documents indexed: %d' % sum(
            idx.get_index(project).doc_count()
                for project in settings.PROJECTS
        )
    )
    # database stats
    print 'Index Database: %s' % db.DATABASE_PATH


def run_server():
    print 'Backend: %s' % settings.DEFAULT_SEARCHER
    print 'Server: %s' % settings.SERVER_TYPE
    # launch web server
    server.run()


def reindex():
    indexer.run(get_app_args())

def run():
    options = get_options()
    # determine app action
    if options.run_tests:
        import tests
        tests.run_all()
    elif options.show_version:
        show_version()
    elif options.show_stats:
        show_stats()
    elif options.run_server:
        run_server()
    elif options.reindex:
        reindex()
    else:
        print 'Use -h to see options.'


if __name__ == '__main__':
    print 'Running sherlock...'
    run()
