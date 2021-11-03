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


'''QA for event sink block.'''

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from event_sink import event_sink
from event_source import event_source

# GWN imports
import pmt
import time
from libgwn.gwnblock_py import mutex_prt     # for mutually exclusive printing


class qa_event_sink (gr_unittest.TestCase):
    '''    QA for event sink block.'''

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None


    def tearDown (self):
        self.tb = None

    def test_1_msg_strobe(self):
        print("\n===  Test 1, with GNU Radio message_strobe\n")
        tst_msg = "--- FROM message strobe, counts messages received."
        src = blocks.message_strobe(pmt.intern(tst_msg), 1000)
        blk_sink = event_sink(ev_count=True)
        self.tb.msg_connect( 
            (src, "strobe"), 
            (blk_sink, blk_sink.ports_in[0].port) )
        #self.tb.run()  # for flowgraphs that will stop on its own!
        self.tb.start() 
        time.sleep(5)
        self.tb.stop()
        self.tb.wait()
        return


    def test_2_event_source(self):
        print("\n===  Test 2,  with GWN event_source\n")
        tst_ev = {'Type':'Data', 'Subtype':'TestData', 'seq_nr':0, \
            'payload':'Testing event sink block'}
        blk_src = event_source(ev_count=4, interval=1.0, ev_dc=tst_ev)
        blk_sink = event_sink(ev_count=False)

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
    gr_unittest.run(qa_event_sink)


