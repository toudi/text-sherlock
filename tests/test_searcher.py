#!/usr/bin/env python
# encoding: utf-8
"""
test_searcher.py
"""

import os
import testcase
from core.sherlock import indexer, searcher
from core.utils import debug
import settings
from test_indexer import TestAppArgs
from path import path

TEST_PROJECT_NAME = "Test project"

class TestSearcher(testcase.BaseTestCase):
    def setUp(self):
        """ Called before each test """
        testcase.BaseTestCase.setUp(self)
        app_args = TestAppArgs()
        self.indexer = indexer.Indexer(app_args)
        self.idx = self.indexer.get_index(TEST_PROJECT_NAME)
        self.idx.clear()
        pass
        
    def tearDown(self):
        """ Called after each test """
        pass
        
    def test_simple_search(self):
        """Tests simple search logic
        """
        # index a file for the search
        path = os.path.join(self.test_dir, 'text/objc_example.m')
        self.idx.index_file(path)
        self.idx.commit()
        # test values
        self.assertEquals(self.idx.doc_count(), 1, 'bad doc count, expected 1 but, found %d' % self.idx.doc_count())
        
        # find something in the file
        results = self.idx.searcher().find_text('key')
        self.assertEquals(len(results), 1, 'wrong hit count, expected 1 but, found %d' % len(results))

    def test_search(self):
        """Tests searching against more than one document
        """
        # index directory
        _dir = path(os.path.join(self.test_dir, "text"))
        num_files_expected = 0
        for _file in _dir.walkfiles():
            if not (_file.endswith('m') or _file.endswith('h')):
                num_files_expected += 1

        self.indexer.index_project(TEST_PROJECT_NAME, settings.PROJECTS[TEST_PROJECT_NAME])
        self.assertTrue(self.idx.doc_count() == num_files_expected, 'bad doc count, expected %d but, indexed %d' % (num_files_expected, self.idx.doc_count()))
        # search
        search_text = 'value'
        searcher = self.idx.searcher() 
        results = searcher.find_text(search_text)
        self.assertTrue(len(results) > 1, 'not enough results from the search, expected more than 1, but found %d' % len(results))
        # search by path
        results = searcher.find_path(os.path.join(self.test_dir, 'text', 'example.c'))
        self.assertEquals(len(results), 1, 'wrong number of results for the path search, expected 1, but found %d' % len(results))


def run():
    testcase.run_all(TestSearcher)
    pass
