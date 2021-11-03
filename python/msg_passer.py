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

'''A message passer block; receives and sends messages with two timeouts.'''


from gnuradio import gr

# GWN imports
from libgwn.gwnblock_py import gwnblock_py        # for all GWN blocks
from libgwn.gwnblock_py import mutex_prt          # for tests


class msg_passer(gwnblock_py):
    '''Receives and sends messages with two timeouts.

    This block receives a message on its input port, and resends it on its output port. It starts resending this messages until a first timeout expires, on which it suspends resending; when a second timeout expires, resending continues.
    '''
    def __init__(self, tout_stop=5.0, tout_restart=8.0):
      '''Message passer constructor.

      @param tout_stop: a timeout to stop resending, in seconds.
      @param tout_restart_ a timeout to restart resending, in seconds.
      '''
      gwnblock_py.__init__(self, name='msg_passer', number_in=1, number_out=1, number_timers=0, number_timeouts=2)

      ## initialize timeouts, start
      self.timeouts[0].timeout = tout_stop
      self.timeouts[0].start()
      self.timeouts[1].timeout = tout_restart
      self.timeouts[1].start()

      self.transmit = True      # if True passes message to next block

      return


    def process_data(self, py_msg):
        '''Sends received message, if timeout stops.

        @param py_msg: message, a Python data type.
        '''

        if py_msg['port'] == 'timeout0':
          self.transmit = False
        elif py_msg['port'] == 'timeout1':
          self.transmit = True
        elif self.transmit == True:
          self.write_out(py_msg, port_nr=0)
          pass
        else:
          pass
        return
