"""
This is a phony __init__.py file, so that nose finds the doctests in this
directory.
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import


from future import standard_library
standard_library.install_aliases()
from builtins import *