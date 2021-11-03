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


'''
A template for a new GWN block creation.

This is the template for the new block code.
'''


from gnuradio import gr

# GWN imports
from libgwn.gwnblock_py import gwnblock_py        # for all GWN blocks
from libgwn.gwnblock_py import mutex_prt          # for tests


class <BLOCK_NAME>(gwnblock_py):
    '''New GWN block in Python, created from template.

    '''
    def __init__(self, <BLOCK_PARS>):
      gwnblock_py.__init__(self, <GWNBLOCK_PARS>)

      ### EXAMPLE CODE

      ## initialize timeouts, start
      #self.timeouts[0].timeout = 5
      #self.timeouts[0].start()
      
      ## initialize timers, start
      #self.timers[0].retry = 5
      #self.timers[0].interval = 1.0
      #self.timers[0].start()
      #...

      return


    def process_data(self, py_msg):
      '''Where message processing happens.

      @param py_msg: message, a Python data type; GWN uses dict.
      '''
      if py_msg == None:
        print("No message received")
      else:
        print("Message received:", py_msg)
      return

