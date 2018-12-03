import os
import sys


class Logging:

    def __init__(self, logdir, runtag):
        if not os.path.exists(logdir):
            os.makedirs(logdir)

        self.logdir = logdir
        self.runtag = runtag
        self.inited = True
        self.files = {}

    def open(self, filename, overwrite=False):
        if self.inited:
            p = self.logdir + '/' + filename
            if os.path.exists(p) and not overwrite:
                return False

            if filename in self.files and not overwrite:
                return False
            elif filename in self.files:
                self.files[filename].close()
            self.files[filename] = open(p, 'w')
            return True
        else:
            return False

    def isopen(self, filename):
        if self.inited:
            if filename in self.files:
                if self.files[filename].closed:
                    return False
                else:
                    return True
            else:
                return False
        else:
            return False

    def close(self, filename):
        if filename not in self.files:
            return False

        if self.files[filename].closed:
            return False

        self.files[filename].close()

        return True

    def write(self, filename, data):
        if filename not in self.files:
            return False

        if self.files[filename].closed:
            return False

        self.files[filename].write(str(data) + '\n')
        self.files[filename].flush()
        return True
