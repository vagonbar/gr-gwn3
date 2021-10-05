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
A block to converta an event into a PDU (Protocol Data Unit).
'''


from gnuradio import gr

# GWN imports
from gwnblock_py import gwnblock_py        # for all GWN blocks
from gwnblock_py import mutex_prt          # for tests
from gwnblock_py import msg_to_pdu            # to convert message to PDU

import pickle
import pmt


class ev_to_pdu(gwnblock_py):
    '''Converts an event (string or dictionary) into a PDU.

Receives an event (a string or a dictionary) on the input port, packs it into a PDU, sends PDU on output port.
    '''

    def __init__(self):
      '''Event to PDU constructor.  '''
      gwnblock_py.__init__(self, name='ev_to_pdu', number_in=1, number_out=0, number_timers=0, number_timeouts=0)

      # register output port for PDUs
      self.message_port_register_out(pmt.intern('pdu'))
      return


    def process_data(self, py_msg):
      '''Receives an event, converts to PDU, writes on PDU output port.

      Serializaes event into bytes with pickle, converts to PDU and sends.
      @param py_msg: message, a Python data type; GWN uses string or dictionary.
      '''
      msg_bytes = pickle.dumps(py_msg)
      msg_pdu = msg_to_pdu(msg_bytes)
      self.message_port_pub( pmt.intern('pdu'), msg_pdu)
      return

