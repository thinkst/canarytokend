from twisted.internet import inotify, reactor
from twisted.python import log
from twisted.python import filepath
from twisted.python._inotify import INotifyError
from twisted.internet.inotify import IN_CREATE
import datetime
import os

class FileSystemWatcher(object):

    def __init__(self, fileName=None):
        self.path = fileName
        self.log_dir = os.path.dirname(os.path.realpath(self.path))
        self.f = None

    def reopenFiles(self, skipToEnd=True):
        if self.f:
            self.f.close()

        try:
            self.f = open(self.path)
            if skipToEnd:
                self.f.seek(0, 2)
        except IOError as e:
            log.err('Cannot open file {file}: {exception}'\
                     .format(file=self.path, exception=e))
            self.f = None

        self.notifier.startReading()
        try:
            self.notifier.ignore(filepath.FilePath(self.path))
        except KeyError:
            pass

        try:
            self.notifier.watch(filepath.FilePath(self.path),
                       callbacks=[self.onChange])
        except INotifyError:
            self.notifier.watch(filepath.FilePath(self.log_dir), mask=IN_CREATE,
                       callbacks=[self.onDirChange])

    def start(self):
        self.notifier = inotify.INotify(reactor=reactor)
        self.reopenFiles()

    def handleLines(self, lines=None):
        pass

    def processAuditLines(self,):
        if not self.f:
            return

        lines = self.f.read().strip().split('\n')

        self.handleLines(lines=lines)


    def onChange(self, watch, path, mask):
        #print path, 'changed', mask # or do something else!
        if mask != 2:
            self.reopenFiles()

        self.processAuditLines()


    def onDirChange(self, watch, path, mask):
        #print path, ' dir changed', mask # or do something else!
        #import pdb; pdb.set_trace()
        try:
            self.notifier.ignore(filepath.FilePath(self.log_dir))
        except KeyError:
            pass

        if mask != 2:
            self.reopenFiles(skipToEnd=False)

        self.processAuditLines()
