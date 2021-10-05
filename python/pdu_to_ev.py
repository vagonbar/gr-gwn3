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
A block to convert a PDU (Protocol Data Unit) into an event.
'''


from gnuradio import gr

# GWN imports
from gwnblock_py import gwnblock_py        # for all GWN blocks
from gwnblock_py import mutex_prt          # for tests
from gwnblock_py import pdu_to_msg
import time                             # for tests

import pickle
import pmt


class pdu_to_ev(gwnblock_py):
    '''Converts a PDU into an event (string or dictionary).

Receives a PDU on the input port, unpacks it into an event (string or dictionary), sends event on output port.
    '''
 
    def __init__(self, ):
      '''PDU to event constructor.'''
      gwnblock_py.__init__(self, name='pdu_to_ev', number_in=0, number_out=1, number_timers=0, number_timeouts=0)

      # register input port for PDUS and set function handler
      self.message_port_register_in(pmt.intern('pdu'))
      self.set_msg_handler(pmt.intern('pdu'), self.handle_pdu_msg)
      return


    def handle_pdu_msg(self, pdu):
        '''Handle function for PDU input port.

        Receives a PDU, deserializes with pickle into a Python data type.
        @param pdu: a PDU.'''
        meta, msg_bytes = pdu_to_msg(pdu)
        py_msg = pickle.loads(msg_bytes)
        self.process_data(py_msg)
        return


    def process_data(self, py_msg):
      '''Receives an event, writes event on output port.'''
      self.write_out(py_msg)
      return

