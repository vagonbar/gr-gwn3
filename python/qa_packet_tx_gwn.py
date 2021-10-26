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

from gnuradio import gr, gr_unittest
# from gnuradio import blocks
from packet_tx_gwn import packet_tx_gwn
from packet_rx_gwn import packet_rx_gwn

from gnuradio import channels
from gnuradio import blocks
import pmt



class qa_packet_tx_gwn(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_instance(self):
        # FIXME: Test will fail until you pass sensible arguments to the constructor


        ### blocks

        self.pkt_tx = packet_tx_gwn()
        print(type(self.pkt_tx))
        self.pkt_rx = packet_rx_gwn()
        print(type(self.pkt_tx))

        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=0.0,
            frequency_offset=0.0,
            epsilon=1.0,
            taps=[1.0],
            noise_seed=0,
            block_tags=True)

        self.blocks_random_pdu_0 = blocks.random_pdu(20, 200, 0xFF, 2)

        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("TEST"), 1000)

        self.blocks_message_debug_0_0_0 = blocks.message_debug(True)

        ### connections

        self.tb.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.blocks_random_pdu_0, 'generate'))
        self.tb.msg_connect((self.blocks_random_pdu_0, 'pdus'), (self.pkt_tx, 'in'))
        self.tb.connect((self.pkt_tx, 0), (self.channels_channel_model_0, 0))
        #self.tb.connect((self.channels_channel_model_0, 0), (self.pkt_rx, 0))
        #self.msg_connect((self.pkt_rx, 'pkt out'), (self.blocks_message_debug_0_0_0, 'print_pdu'))

        #self.tb.run()




    def test_001_descriptive_test_name(self):
        # set up fg
        self.tb.run()
        # check data


if __name__ == '__main__':
    gr_unittest.run(qa_packet_tx_gwn)
