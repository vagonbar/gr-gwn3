#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2015-2021
#   Instituto de Ingenieria Electrica, Facultad de Ingenieria,
#   Universidad de la Republica, Uruguay.
#   https://iie.fing.edu.uy/
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
#

'''QA for GWN version of GR packet_tx.
'''

from gnuradio import gr, gr_unittest
# from gnuradio import blocks
from packet_tx_gwn import packet_tx_gwn
from packet_rx_gwn import packet_rx_gwn
from pdu_to_ev import pdu_to_ev
from ev_to_pdu import ev_to_pdu
from event_sink import event_sink
from event_source import event_source

from gnuradio import channels
from gnuradio import blocks
from gnuradio import pdu
import pmt
import time

import signal

class qa_packet_tx_gwn(gr_unittest.TestCase):
    '''QA for GWN version of GR packet_tx.
    '''

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_gr_packet(self):
        '''Packet Tx and Packet Tx with GR blocks.
        '''
        print("\n=== Packet Tx Rx with GR blocks")

        ### blocks
        pkt_tx = packet_tx_gwn()
        pkt_rx = packet_rx_gwn()
        channel_model = channels.channel_model(
            noise_voltage=0.0,
            frequency_offset=0.0,
            epsilon=1.0,
            taps=[1.0],
            noise_seed=0,
            block_tags=True)
        random_pdu = pdu.random_pdu(20, 200, 0xFF, 2)
        multiply_const = blocks.multiply_const_cc(1.0)
        message_strobe = blocks.message_strobe(pmt.intern("TEST"), 1000)
        message_debug = blocks.message_debug(True)

        ### connections
        self.tb.msg_connect((message_strobe, 'strobe'), (random_pdu, 'generate'))
        self.tb.msg_connect((random_pdu, 'pdus'), (pkt_tx, 'in'))
        self.tb.connect((pkt_tx, 0), (channel_model, 0))
        self.tb.connect((channel_model, 0), (multiply_const, 0))
        self.tb.connect((multiply_const, 0), (pkt_rx, 0))
        self.tb.msg_connect((pkt_rx, 'pkt out'), (message_debug, 'print'))
        #self.tb.run()
        self.tb.start()
        time.sleep(6)
        self.tb.stop()
        self.tb.wait()

        return



if __name__ == '__main__':
    gr_unittest.run(qa_packet_tx_gwn)
