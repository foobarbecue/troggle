import settings
import expo.models as models
import re
import os

def readFile(filename):
    for line in fileIterator(settings.SURVEX_DATA, filename):
        print line

re_include_extension = re.compile(r"^\s*\*include\s+([^\s]*).svx$", re.IGNORECASE)
re_include_no_extension = re.compile(r"^\s*\*include\s+([^\s]*)$", re.IGNORECASE)

def fileIterator(directory, filename):
    f = open(os.path.join(directory, filename + ".svx"), "rb")
    for line in f.readlines():
        include_extension = re_include_extension.match(line)
        include_no_extension = re_include_no_extension.match(line)
        def a(include):
            link = re.split(r"/|\\", include)
            print os.path.join(directory, *link[:-1]), link[-1]
            return fileIterator(os.path.join(directory, *link[:-1]), link[-1])
        if include_extension:
            for b in a(include_extension.groups()[0]):
                yield b
        elif include_no_extension:
            for b in a(include_no_extension.groups()[0]):
                yield b
        else:
            yield line

readFile("all")