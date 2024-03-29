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


'''QA for message sink block.'''

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from msg_sink import msg_sink
from msg_source import msg_source

import pmt
import time
from libgwn.gwnblock_py import mutex_prt


class qa_msg_sink (gr_unittest.TestCase):
    '''QA for message sink block.'''

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_msg_strobe(self):
        print("\n===  Test 1, with GNU Radio message_strobe\n")
        tst_msg = "--- FROM message strobe TO msg_sink"
        src = blocks.message_strobe(pmt.intern(tst_msg), 1000)
        blk_sink = msg_sink()

        self.tb.msg_connect( 
            (src, "strobe"), 
            (blk_sink, blk_sink.ports_in[0].port) )

        #self.tb.run()  # for flowgraphs that will stop on its own!
        self.tb.start() 
        time.sleep(5)
        self.tb.stop()
        self.tb.wait()

        return

    def test_msg_source(self):
        print("\n===  Test 2,  with GWN msg_source\n")
        tst_msg = "--- FROM message source TO msg_sink"
        blk_src = msg_source(msg_count=4, interval=1.0)
        blk_sink = msg_sink()

        self.tb.msg_connect( 
            (blk_src, blk_src.ports_out[0].port), 
            (blk_sink, blk_sink.ports_in[0].port) )

        #self.tb.run()  # for flowgraphs that will stop on its own!
        self.tb.start() 

        time.sleep(5)

        self.tb.stop()
        self.tb.wait()

        return


if __name__ == '__main__':
    gr_unittest.run(qa_msg_sink)


