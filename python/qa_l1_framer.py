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


'''QA for l1_framer block.'''

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from gwnblock_py import gwnblock_py
from l1_framer import l1_framer

from msg_source import msg_source
from event_source import event_source

import pmt
import time
from gwnblock_py import mutex_prt     # for mutually exclusive printing


class qa_l1_framer (gr_unittest.TestCase):
    '''QA for l1_framer block.
    '''
    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_l1_framer(self):
        print ("\n=== Test message L1 framing")
        #blk_src = msg_source(msg_count=5, interval=1.0)
        #blk_src.timers[0].debug = False     # True
        blk_src = event_source(ev_count=5, interval=1.0, ev_dc="PRUEBA")
        blk_pass =l1_framer(in_type='payload')
        blk_dbg = blocks.message_debug()

        self.tb.msg_connect( 
            (blk_src, blk_src.ports_out[0].port), 
            (blk_pass, blk_pass.ports_in[0].port) )
        self.tb.msg_connect( 
            (blk_pass, 'pdu'), 
            (blk_dbg, 'print') )

        #self.tb.run()  # for flowgraphs that will stop on its own!
        self.tb.start() 
        time.sleep(8)
        self.tb.stop()
        self.tb.wait()

        return


if __name__ == '__main__':
    gr_unittest.run(qa_l1_framer)


