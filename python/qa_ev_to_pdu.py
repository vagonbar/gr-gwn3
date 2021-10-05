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
QA for ev_to_pdu.
'''


from gnuradio import gr, gr_unittest
from gnuradio import blocks
from gwnblock_py import gwnblock_py

from ev_to_pdu import ev_to_pdu
from msg_source import msg_source

import pmt
import time
from gwnblock_py import mutex_prt     # for mutually exclusive printing


class qa_ev_to_pdu (gr_unittest.TestCase):
    '''QA for ev_to_pdu.'''

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_ev_to_pdu(self):
        '''Tests with GWN msg_source and GR message_debug.

        Flowgraph: Message source --> Event to PDU --> Message debug.'''

        blk_src = msg_source(msg_count=10, interval=1.0)   # source
        blk_ev2pdu = ev_to_pdu()                           # convert to PDU
        blk_snk = blocks.message_debug()                   # sink

        self.tb.msg_connect(blk_src, blk_src.ports_out[0].port, 
                            blk_ev2pdu, blk_ev2pdu.ports_in[0].port)
        self.tb.msg_connect(blk_ev2pdu, 'pdu',
                            blk_snk, 'print_pdu')

        #self.tb.run()  # for flowgraphs that will stop on its own!
        self.tb.start() 
        #mutex_prt(self.tb.msg_edge_list())
        #print tb.dump()
        time.sleep(12)    # to allow for Message source to finish
        self.tb.stop()
        self.tb.wait()

        return


if __name__ == '__main__':
    gr_unittest.run(qa_ev_to_pdu)


