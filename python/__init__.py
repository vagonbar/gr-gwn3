#!/usr/bin/env python3
#-*- coding: utf-8 -*-
# 
# Copyright 2015-2021
#    Instituto de Ingenieria Electrica, Facultad de Ingenieria,
#    Universidad de la Republica, Uruguay.
#    https://iie.fing.edu.uy/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#


# The presence of this file turns this directory into a Python package

'''
GNU Radio GWN3 Python blocks and tests.

For the GWN3 library, please see the libgwn directory.
Pure Python blocks require an import in this file __init__.py, of the form::

    from .block_name import block_name

This is necessary to have the new block included in the C{gwn3} package.
'''

from __future__ import unicode_literals

# import swig generated symbols into the gwn3 namespace
try:
    # this might fail if the module is python-only
    from .gwn3_swig import *
except ImportError:
    pass
except:
    pass

# import any pure python here
from .gwnblock_py import gwnblock_py
from .msg_source import msg_source
from .msg_sink import msg_sink
from .msg_passer import msg_passer

from .virtual_channel import virtual_channel







#
