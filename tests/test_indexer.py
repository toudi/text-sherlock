#!/usr/bin/env python
# encoding: utf-8
"""
test_indexer.py
"""

import os
import testcase
from core.sherlock import indexer
from path import path
import settings
from core.sherlock.db import ProjectMeta
from subprocess import call

class TestAppArgs:
    reindex = 'rebuild'
    verbose = False


TEST_PROJECT_NAME = "Test project"
GIT_PROJECT_NAME  = "Git project"


class TestIndexer(testcase.BaseTestCase):
    def setUp(self):
        self.TEST_PROJECT      = settings.PROJECTS[TEST_PROJECT_NAME]
        self.GIT_PROJECT       = settings.PROJECTS[GIT_PROJECT_NAME]

        """ Called before each test """
        testcase.BaseTestCase.setUp(self)
        app_args = TestAppArgs()
        self.indexer = indexer.Indexer(app_args)
        self.idx = self.indexer.get_index(TEST_PROJECT_NAME, self.TEST_PROJECT)
        self.idx.clear()
        pass

    def tearDown(self):
        """ Called after each test """
        pass

    def test_indexer_creation(self):
        """Test indexer creation logic
        """
        # the below call provides and sets up a default indexer environment
        # based on the settings.py script values
        # the index name (usually 'main') has been overriden for testing
        # test values
        self.assertFalse(self.indexer is None, 'unable to create an indexer')
        
    def test_index_file(self):
        """Tests file indexing logic
        """
        # first, test if the doc count is 0. It's an empty index, so that should pass.
        self.assertEquals(self.idx.doc_count(), 0, 'Bad initial doc count: %d' % self.idx.doc_count())
        # now, let us index some *.c files.
        self.idx.index_file(os.path.join(self.test_dir, 'text/example.c'))
        self.idx.commit()
        self.assertEquals(self.idx.doc_count(), 1, 'file suffix recognition failed! (\'.c\') doc-count: %d' % self.idx.doc_count())
        
    def test_index_directory(self):
        """Tests directory content indexing logic
        """
        _dir = path(os.path.join(self.test_dir, "text"))
        num_files_expected = 0
        for _file in _dir.walkfiles():
            if not (_file.endswith('m') or _file.endswith('h')):
                num_files_expected += 1

        self.indexer.index_project(TEST_PROJECT_NAME, self.TEST_PROJECT)
        self.assertTrue(self.idx.doc_count() == num_files_expected, 'bad doc count, expected %d but, indexed %d' % (num_files_expected, self.idx.doc_count()))

    def test_index_git_project(self):
        git_idx = self.indexer.get_index(GIT_PROJECT_NAME, self.GIT_PROJECT)
        self.indexer.index_project(GIT_PROJECT_NAME, self.GIT_PROJECT)
        self.assertEquals(git_idx.doc_count(), 2, 'Expected 2 files in test git project, but found %d instead' % git_idx.doc_count())

    def test_index_between_commits(self):
        call([
            'rm',
            '-rf',
            os.path.dirname(__file__) + '/../src/Git project'
        ])
        # git_idx = self.indexer.get_index(GIT_PROJECT_NAME, self.GIT_PROJECT)
        # v2_path = 'new-file-in-v2.txt'
        # v1_sha = 'e8dae9983fb33b268a566aab69a3c4867d93f234'
        # #let's check if git only indexes one file after pulling.

        # searcher = git_idx.searcher()
        # # this file is added only in v2 tag, therefore it should not be present
        # self.assertEquals(len(searcher.find_path(v2_path)), 0, 'file from v2 tag is already in the index')

        # project = ProjectMeta.select().where(ProjectMeta.name == GIT_PROJECT_NAME).get()
        # project.rev = v1_sha
        # project.save()

        # self.indexer.index_project(GIT_PROJECT_NAME, self.GIT_PROJECT)

        # self.assertEquals(len(searcher.find_path(v2_path)), 1, 'file from v2 tag doesn\'t appear to be in the index')
        # project = ProjectMeta.select().where(ProjectMeta.name == GIT_PROJECT_NAME).get()
        # last_rev = project.rev

        # self.assertEquals(last_rev, v1_sha, 'git didn\'t update the sha after indexing!')


def run():
    testcase.run_all(TestIndexer)
    pass
