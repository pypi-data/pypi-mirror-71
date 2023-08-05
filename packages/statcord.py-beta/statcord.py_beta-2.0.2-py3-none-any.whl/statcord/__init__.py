__title__ = 'statcord.py-beta'
__author__ = 'statcord.com'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020, statcord.com'
__version__ = '2.0.2'

name = "statcordbeta"

from collections import namedtuple
from .client import Client
from .exceptions import *

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')

version_info = VersionInfo(major=2, minor=0, micro=2, releaselevel='final', serial=0)
