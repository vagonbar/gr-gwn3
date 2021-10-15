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


'''L1 framer, adds prefix and postfix fields for L1 framing.'''


from gnuradio import gr
import pmt

import pickle

from gwnblock_py import gwnblock_py        # for all GWN blocks
from gwnblock_py import mutex_prt          # for tests
from gwnblock_py import msg_to_pdu         # converts Python data type into PDU
from libgwn import gwnutils



class l1_framer(gwnblock_py):
    '''Adds prefix and postfix fields for L1 framing.

    Receives an event on input port, adds access code, length, and CRC32 for L1 framing; sends on output port a PDU (Protocol Data Unit). Framing may be done on the event (dictionary) previously serialized, on the payload (string or byte sequence), or on a received PMT message; received data type is indicated by in_type parameter.

    @param in_type: type of input, may be "event", "payload", or "pmt_msg".
    '''

    def __init__(self, in_type='event'):
        '''L1 framer constructor.'''
        gwnblock_py.__init__(self, name='l1_framer', number_in=1, number_out=0, number_timers=0, number_timeouts=0)

        self.in_type = in_type
        '''Type of message received, from parameter in_type.'''
      
        # values for encoding
        self._samp_per_sym = 5
        self._bits_per_sym = 2
        self._preamble = gwnutils.default_preamble
        self._access_code = gwnutils.default_access_code
        self._pad_for_usrp = True
        self._whitener_offset = False

        # register output port for PDUs
        self.message_port_register_out(pmt.intern('pdu'))

        return


    def process_data(self, py_msg):
        '''Adds framing fields, creates PDU, writes on output.

        @param py_msg: message, a Python data type.
        '''

        # create string to send
        if self.in_type == 'event':
            send_str = pickle.dumps(py_msg)    # serializes dictionary
        elif self.in_type == 'payload':
            send_str = py_msg                  # string or bytes go as such
        elif self.in_type == 'pmt_msg':
            send_str = py_msg                  # a PMT message goes as such

        if self.debug:
            msg_dbg = '--- L1 framer, id {0}\n'.format(id(self),)
            msg_dbg += '[Send str] : ' + repr(send_str) + '\n'
            msg_dbg += '[Send str len] : ' + str(len(send_str)) + '\n'
            mutex_prt(msg_dbg)

        # frame packet
        send_pkt = gwnutils.make_packet(send_str,
            self._samp_per_sym,
            self._bits_per_sym,
            self._preamble,
            self._access_code,
            self._pad_for_usrp,
            self._whitener_offset)

        pdu = msg_to_pdu(send_pkt) #, debug=self.debug)
        self.message_port_pub( pmt.intern('pdu'), pdu)

        return



