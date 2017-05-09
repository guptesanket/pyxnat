from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from builtins import str
import os


def find_files(src):
    names = os.listdir(src)

    errors = []
    files = []

    for name in names:
        srcname = os.path.join(src, name)
        try:
            if os.path.islink(srcname):
                linkto = os.readlink(srcname)
                files.extend(find_files(linkto))
                # os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                files.extend(find_files(srcname))
            else:
                files.append(srcname)
        except (IOError, os.error) as why:
            errors.append((srcname, str(why)))

    return files


def ensure_dir_exists(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return os.path.isdir(dir_path)
