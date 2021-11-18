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

'''An event sink block, prints events received.'''


from gnuradio import gr

# GWN imports
from libgwn.gwnblock_py import gwnblock_py        # for all GWN blocks
from libgwn.gwnblock_py import mutex_prt          # for tests


class event_sink(gwnblock_py):
    '''Receives an event and shows its content.

    @ivar ev_count: if True, counts evens received.
    @ivar ev_counter: a counter, for optionally show numer of message received.
    '''
    def __init__(self, ev_count=False):
      '''Event sink constructor.

      @param ev_count: if True, counts events received and prints this number before the event contents.
      '''
      gwnblock_py.__init__(self, name='event_sink', number_in=1, number_out=0, number_timers=0, number_timeouts=0)
      self.ev_count = ev_count
      self.ev_counter = 0
      return


    def process_data(self, py_msg):
      '''Prints received event.

      @param py_msg: message, a Python data type; GWN uses dict.
      '''
      if self.ev_count:
          self.ev_counter += 1
          prt_msg =  "*** Message received " + str(self.ev_counter) + " ***\n"
          prt_msg += str(py_msg)
          prt_msg += "\n************************"
      else:
          prt_msg = str(py_msg)
      mutex_prt(prt_msg)
      return

