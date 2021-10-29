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

'''A message source block, emits messages at regular intervals.'''


from gnuradio import gr

# GWN imports
from gwnblock_py import gwnblock_py        # for all GWN blocks
from gwnblock_py import mutex_prt          # for tests


class msg_source(gwnblock_py):
    '''Emits a number of messages at regular intervals.
    '''
    def __init__(self, msg_count=10, interval=1.0, ev_fields=""):
      '''Message source constructor.

      @param msg_count: the number of messages to emit.
      @param interval: the lapse of time between messages, in seconds.
      @param ev_fields: event fields, may by a dictionary or just a string.
      '''
      gwnblock_py.__init__(self, name='msg_source', number_in=0, number_out=1, number_timers=1, number_timeouts=0)

      ## initialize timers, start
      self.timers[0].retry = msg_count 
      self.timers[0].interval = interval
      #self.timers[0].exit_flag = False
      #self.timers[0].interrupt = False
      self.timers[0].msg_dc_1['Final'] = 'False'
      self.timers[0].msg_dc_2['Final'] = 'True'
      self.timers[0].msg_dc_1['payload'] = ev_fields
      self.timers[0].msg_dc_2['payload'] = ev_fields
      self.start_timers()

      return


    def process_data(self, py_msg):
        '''Sends message receivedfrom timer.

        @param py_msg: message, a Python data type.
        '''
        self.write_out(py_msg, port_nr=0)
        return
