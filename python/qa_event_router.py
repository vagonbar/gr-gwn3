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


'''QA for event router block.'''

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from event_router import event_router

from event_sink import event_sink
from event_source import event_source

import time
from libgwn.gwnblock_py import mutex_prt     # for mutually exclusive printing


class qa_event_router (gr_unittest.TestCase):
    '''
    QA for new GWN block in Python, created from template.
    '''
    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_event_router(self):

        print ("\n=== Test event router")
        blk_src_0 = event_source(ev_count=6, interval=0.5, \
            ev_dc={'Type':'Data', 'Subtype':'Test_0'} )
        blk_src_1 = event_source(ev_count=3, interval=1.0, \
            ev_dc={'Type':'Data', 'Subtype':'Test_1'} )
        blk_pass = event_router('Subtype', 'Test_0', 'Subtype', 'Test_1')
        blk_sink = event_sink(ev_count=True)
        blk_sink_1 = event_sink(ev_count=True)

        self.tb.msg_connect( 
            (blk_src_0, blk_src_0.ports_out[0].port), 
            (blk_pass, blk_pass.ports_in[0].port) )
        self.tb.msg_connect( 
            (blk_src_1, blk_src_1.ports_out[0].port), 
            (blk_pass, blk_pass.ports_in[0].port) )
        self.tb.msg_connect( 
            (blk_pass, blk_pass.ports_out[0].port), 
            (blk_sink, blk_sink.ports_in[0].port) )
        self.tb.msg_connect( 
            (blk_pass, blk_pass.ports_out[1].port), 
            (blk_sink_1, blk_sink_1.ports_in[0].port) )

        #self.tb.run()  # for flowgraphs that will stop on its own!
        self.tb.start() 

        mutex_prt(self.tb.msg_edge_list())
        #print(tb.dump())

        time.sleep(8)
        self.tb.stop()
        self.tb.wait()

        return


if __name__ == '__main__':
    gr_unittest.run(qa_event_router)


