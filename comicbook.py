from zipfile import *
# import rarfile
from pyunpack import *
from tempfile import TemporaryDirectory
import os

class ComicBookFile:
    'A CBZ or CBR file containing a comic book'

    def __init__(self, path):
        self.path = path
        self.type = path.split('.')[-1]
        self.images = []

    def unzip(self):
        ZipFile(self.path).extractall('/tmp/123456')

    def unrar(self):
         dir = TemporaryDirectory()
         Archive(self.path).extractall(dir.name)
         for path, subdirs, files in os.walk(dir.name):
             for name in files:
                 if name.split('.')[-1].lower() == 'jpg':
                     self.images.append(os.path.join(path, name))
         print(self.images)
         return ComicBook(dir, self.images)

class ComicBook:
    def __init__(self, tempdir, images, startpage=0):
        self.tempdir = tempdir
        self.images = images
        self.current_page = startpage
        self.total_pages = len(self.images) - 1

    def flip_page(self, direction):
        directions = {'next': 1, 'prev': -1}
        self.current_page += directions[direction]

