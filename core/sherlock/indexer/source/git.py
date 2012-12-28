from settings import ROOT_DIR
from subprocess import check_output, call, STDOUT
import os
from path import path
from core.sherlock.db import ProjectMeta
from . import IndexSource


class Git(IndexSource):
    def __init__(self, project, url, branch='master',
                 username=None, password=None):
        self.branch = branch
        self.project = project
        self.url = url
        self.indexer = None
        self._index = None
        self.git_diff_info = 'git log %s..HEAD --pretty="format:" --name-status | egrep \'^%s\' | cut -f 2'
        self._last_rev = None

    def get_last_rev(self):
        if not self._last_rev:
            src_path = path("%s/%s" % (ROOT_DIR, "src"))
            if not src_path.exists():
                src_path.makedirs(0755)
            repo = src_path / self.project
            if not repo.exists():
                call([
                    'git', 'clone', self.url, repo
                ])
            else:
                os.chdir(repo)
                call(['git', 'pull'])

            with open('/dev/null', 'w') as devn:
                call(['git', 'checkout', 'origin/%s' % self.branch], stdout=devn, stderr=devn)

            self.head = check_output(['git', 'rev-parse', 'HEAD']).strip('\n')

            #read last index info.
            last_rev = ProjectMeta.select().where(ProjectMeta.name == self.project)
            if not last_rev.exists():
                last_rev = None
            else:
                last_rev = last_rev.get().rev.strip('\n')
                #print(last_rev.__dict__)

            self._last_rev = last_rev

        return self._last_rev

    def get_files_for_removal(self, mode='update'):
        if mode == 'rebuild':
            return ()

        last_rev = self.get_last_rev()

        if last_rev:
            return check_output(
                self.git_diff_info % (last_rev, 'D'),
                shell=True
            ).split('\n')

        return ()

    def get_files_for_index(self, mode='update'):
        last_rev = self.get_last_rev()

        if last_rev is None or mode == 'rebuild':
            return check_output(['git', 'ls-files']).split('\n')

        return check_output(
            self.git_diff_info % (last_rev, '(A|M)'),
            shell=True
        ).split('\n')

    def indexing_finished(self):
        project = ProjectMeta.select().where(ProjectMeta.name == self.project)
        if not project.exists():
            ProjectMeta.create(
                name=self.project,
                rev=self.head
            )
        else:
            if self.head != self.get_last_rev():
                project = project.get()
                project.rev = self.head
                project.save()
