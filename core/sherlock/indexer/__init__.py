from settings import PROJECTS, INDEXING_BACKEND
import logging
from core.utils import import_by_name
import re

__all__ = [
    'run'
]


class Indexer(object):
    def __init__(self, app_args):
        self._log = None
        self.app_args = app_args
        #Separate instances in case anyone would like to multi-thread the indexing
        self.backends = {}
        self.file_allow = {}
        self.file_exclude = {}

        logging_cfg = {
            'level': logging.CRITICAL,
            'format': '%(asctime)-15s %(levelname)s %(message)s'
        }

        if app_args.verbose:
            logging_cfg['level'] = logging.DEBUG
        logging.basicConfig(**logging_cfg)

    def run(self):
        """
        This is the entry point for indexing / rebuilding all of the indexes.
        """
        if self.app_args.reindex == 'rebuild':
            wait_time = 5  # seconds to wait/pause until rebuilding index
            print 'Reindexing everything!'
            print 'Waiting %ss for interrupt...' % wait_time
            import time
            time.sleep(wait_time)

        for project, options in PROJECTS.items():
            logging.debug('-> indexing project "%s"', project)
            source_engine = import_by_name(options['SOURCE'])
            options['SETTINGS']['project'] = project
            source = source_engine(**options['SETTINGS'])
            source.index(self)

    def log(self, *args):
        logging.debug(*args)

    def get_index(self, project):
        if project not in self.backends:
            backend = import_by_name(INDEXING_BACKEND)
            if 'BACKEND' in PROJECTS[project]:
                backend = import_by_name(PROJECTS[project]['BACKEND'])
            self.backends[project] = backend(project=project)
        return self.backends[project]

    def is_allowed(self, project, _file):
        if not project in self.file_exclude:
            self.file_exclude[project] = None
            self.file_allow[project] = None
            if len(PROJECTS[project].get('EXCLUDE_FILE_SUFFIX', [])) > 0:
                self.file_exclude[project] = re.compile("\.(%s)$" % '|'.join(PROJECTS[project]['EXCLUDE_FILE_SUFFIX']))
            if len(PROJECTS[project].get('INCLUDE_FILE_SUFFIX', [])) > 0:
                self.file_allow[project] = re.compile("\.(%s)$" % '|'.join(PROJECTS[project]['INCLUDE_FILE_SUFFIX']))

        if _file.basename().startswith('.'):
            return False

        if self.file_exclude[project] and self.file_exclude[project].search(_file.basename()):
            return False

        if self.file_allow[project] and self.file_allow[project].search(_file.basename()):
            return True

        return self.file_allow[project] is None


def run(app_args):
    indexer = Indexer(app_args)
    return indexer.run()
