from path import path as _path
from core.utils import resolve_path


class FileSystem(object):
    def __init__(self, path, project, recursive=False):
        if '%(sherlock_dir)s' in path:
            path = resolve_path(path)
        self.path = _path(path)
        self.recursive = recursive
        self.project = project
        self.indexer = None
        self._index = None

    def index(self, indexer):
        self.indexer = indexer
        self._index = indexer.get_index(self.project)
        self._index.begin()
        if self.indexer.app_args.reindex == 'rebuild':
            self._index.create_index()
        self.scan(self.path)
        #please note, that only the FileSystem source uses the clean_index method.
        #other sources (such as git/svn) remove files from the index manually, as needed.
        self._index.clean_index()
        self._index.commit()

    def scan(self, _dir):
        for _file in _dir.files():
            if self.indexer.is_allowed(self.project, _file):
                self.indexer.log(":: Adding file '%s' to index", _file)
                self._index.index_file(_file)
        if self.recursive:
            for _dir_ in _dir.dirs():
                if self.indexer.is_allowed(self.project, _dir_):
                    self.indexer.log(":: Scanning '%s' dir..", _dir_)
                    self.scan(_path(_dir_))
