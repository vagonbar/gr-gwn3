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

'''An event source block, emits events at regular intervals.'''


from gnuradio import gr

# GWN imports
from libgwn.gwnblock_py import gwnblock_py        # for all GWN blocks
from libgwn.gwnblock_py import mutex_prt          # for tests


class event_source(gwnblock_py):
    '''Emits a number of user defined events at regular intervals.
    '''
    def __init__(self, ev_count=10,interval=1.0,ev_dc={}):
      '''Event source constructor.

      Events are Python dictionaries with keys and values defined by user.
      @param ev_count: the number of events to emit.
      @param interval: the lapse of time between events, in seconds.
      @param ev_dc: usually a dictionary, the user defined events to generate, may also be a string.
      '''
      gwnblock_py.__init__(self, name='event_source', number_in=0, number_out=1, number_timers=1, number_timeouts=0)

      self.ev_dc = ev_dc
      '''Event to emit, a dictionary.'''
      self.seq_nr = 0
      '''An optional sequence number to include in event to emit.'''

      ## initialize timers, start
      self.timers[0].retry = ev_count
      self.timers[0].interval = interval
      self.start_timers()
      return


    def process_data(self, py_msg):
      '''Sends user defined event when timer message received.

      @param py_msg: message received from timer.
      '''
      if 'seq_nr' in self.ev_dc:
        self.seq_nr += 1
        self.ev_dc['seq_nr'] = self.seq_nr
      self.write_out(self.ev_dc, port_nr=0)
      return

