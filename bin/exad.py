#! python
# http://infohost.nmt.edu/tcc/help/lang/python/sysprog.html
# http://docs.python.org/library/stat.html
# http://effbot.org/zone/python-fileinfo.htm

import sys; sys.path.append('') # where are repos?

from os.path import isdir
from Piping import Pipe
from Piping.iterpipe import ShellPipe
from Piping.commands import *

cal = ShellPipe('cal')

tfdir = '' # tfdir

# from http://jeetworks.com/node/62
class cached_property(object):
    """
    Lazy-loading read/write property descriptor.
    Value is stored locally in descriptor object. If value is not set when
    accessed, value is computed using given function. Value can be cleared
    by calling 'del'.
    """
 
    def __init__(self, func):
        self._func = func
        self._values = {}
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__
 
    def __get__(self, obj, obj_class):
        if obj is None:
            return obj
        if obj not in self._values \
                or self._values[obj] is None:
            self._values[obj] = self._func(obj)
        return self._values[obj]
 
    def __set__(self, obj, value):
        self._values[obj] = value
 
    def __delete__(self, obj):
        if self.__name__ in obj.__dict__:
            del obj.__dict__[self.__name__]
        self._values[obj] = None

class PipingFile():
    def __init__(self, *pathstr):
        if len(pathstr) == 1:
            self.basepath, self.name = split(pathstr)
        else:
            (self.basepath, self.name) = pathstr
    @cached_property
    def isdir(self):
        return isdir(self.fullpath)
    @cached_property
    def fullpath(self):
        return join(self.basepath, self.name)
    @cached_property
    def filetype(self):
        return (None |ShellPipe("file {}")(self.fullpath)).next().split(': ',1)[1]
    @cached_property
    def stats(self):
        pass
    # iterpipes doesn't fully shell escape?
    def __repr__(self):
        return self.name
    # add other stats.

from os import listdir
from os.path import join, split
@Pipe
def lsdirs(inp):
    if type(inp) in (str,unicode):
        inp = (inp,)
    for d in inp:
        for i in listdir(d):
            yield PipingFile(d, i)

#thedirs = (tfdir,) | lsdirs | where(isdir) | a(tuple)
# where attr? pass pipes to where?

thefiles = (tfdir,) | lsdirs
thedirs = thefiles | where(lambda x: x.isdir)
thedirs | each(lambda x: x.filetype) | ppout



rars = []
smalldirs = []

# for d in thedirs:
#     ld = listdir(d)
#     thefiles = \
#     ( ftype(join(d,l)) | select(lambda x: tuple(x.split(': ',1)))
#       for l in ld if len(ld) < 30 ) \
#           | chain | as_list
#     if thefiles and len(thefiles) < 4:
#         smalldirs.append(thefiles)
#     rars += \
#     thefiles | where(lambda (x,y): y.startswith('RAR')) \
#              | select(lambda (x,y): x) | as_list

    

#thefiles | where(lambda (x,y): y.find('MPEG') != -1) | ppout

#thedirs = thefiles | where(lambda (x,y): y == 'directory') | as_tuple

#for d in thedirs | select(lambda (x,y): tuple(glob(x +'/*'))):
#    d | where(lambda x: x.endswith('rar')) | ppout


#thebuzz = thefiles | each(ShellPipe('file {}'))
# each for python functions (strip) and for shellpipes (file)

#print [ i for i in thebuzz]

#take dir
#aunpack $1/*.rar && rm -r $1
