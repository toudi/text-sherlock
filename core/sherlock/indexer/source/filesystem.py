from path import path as _path
from core.utils import resolve_path
from . import IndexSource
from ...db import IndexerMeta
import os
from datetime import datetime
from settings import PROJECTS


class FileSystem(IndexSource):
    def __init__(self, path, project, recursive=False):
        if '%(sherlock_dir)s' in path:
            path = resolve_path(path)
        self.path = _path(path)
        self.recursive = recursive
        self.project = project
        self.indexer = None
        self._index = None
        self._files = {}

    def get_files_for_index(self, mode='update'):
        if mode == 'rebuild':
            IndexerMeta.delete().execute()
        self.scan(self.path, mode)
        return self._files.keys()

    def scan(self, _dir, mode='update'):
        for _file in _dir.files():
            mtime = datetime.fromtimestamp(os.stat(_file).st_mtime)
            f = IndexerMeta.select().where(
                IndexerMeta.project == self.project,
                IndexerMeta.path == _file
            )
            if f.exists():
                if f.get().mod_date < mtime or mode == 'rebuild':
                    self._files[_file] = mtime
            else:
                self._files[_file] = mtime

        if self.recursive:
            for _dir_ in _dir.dirs():
                self.scan(_path(_dir_), mode)

    def indexing_finished(self):
        now = datetime.now()
        self._index.clean_index()

        for _file, mtime in self._files.items():
            f = IndexerMeta.select().where(
                IndexerMeta.project == self.project,
                IndexerMeta.path == _file
            )

            if f.exists():
                f = f.get()
            else:
                f = IndexerMeta(
                    project=self.project,
                    path=_file,
                    date_added=now
                )
            f.mod_date = mtime
            f.save()

    @staticmethod
    def get_root_path(project):
        return resolve_path(PROJECTS[project]['settings']['path'])