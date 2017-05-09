from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
import os

from .. import Interface

_modulepath = os.path.dirname(os.path.abspath(__file__))

central = Interface(config=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'central.cfg'))

def test_global_scan_listing():
    assert central.array.scans(project_id='CENTRAL_OASIS_CS', 
                               experiment_type='xnat:mrSessionData', 
                               scan_type='xnat:mrScanData'
                               )

