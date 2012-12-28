from path import path
class IndexSource(object):
    def index(self, indexer):
        self.indexer = indexer
        self._index = indexer.get_index(self.project)
        self._index.begin()

        if self.indexer.app_args.reindex == 'rebuild':
            self._index.create_index()

        for _file in self.get_files_for_index(self.indexer.app_args.reindex):
            _file = path(_file)
            if self.indexer.is_allowed(self.project, _file):
                self.indexer.log(":: Adding file '%s' to index", _file)
                self._index.index_file(_file)

        for _file in self.get_files_for_removal(self.indexer.app_args.reindex):
            _file = path(_file)
            if self.indexer.is_allowed(self.project, _file):
                self.indexer.log(":: Removing file '%s' from index", _file)
                self._index.remove_file(_file)

        self._index.commit()
        self.indexing_finished()

    def indexing_finished(self):
        pass

    def get_files_for_index(self, mode='update'):
        return ()

    def get_files_for_removal(self, mode='update'):
        return ()
