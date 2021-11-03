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
QA for pdu_to_ev.
'''


from gnuradio import gr, gr_unittest
from gnuradio import blocks
from pdu_to_ev import pdu_to_ev

# GWN imports
from ev_to_pdu import ev_to_pdu
from msg_source import msg_source
#from data_source import data_source
from msg_sink import msg_sink

#import pmt
import time
from libgwn.gwnblock_py import mutex_prt     # for mutually exclusive printing


class qa_pdu_to_ev (gr_unittest.TestCase):
    '''QA for pdu_to_ev.'''

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_pdu_to_ev(self):
        '''Tests with GWN msg_source, ev_to_pdu, msg_sink.

        Flowgraph: Message source --> Event to PDU --> PDU to event --> Message sink.'''

        blk_src = msg_source(msg_count=4, interval=1.0)
        blk_ev2pdu = ev_to_pdu()
        blk_pdu2ev = pdu_to_ev()
        blk_snk = msg_sink()

        self.tb.msg_connect(blk_src, blk_src.ports_out[0].port, 
                            blk_ev2pdu, blk_ev2pdu.ports_in[0].port )
        self.tb.msg_connect(blk_ev2pdu, 'pdu',
                            blk_pdu2ev, 'pdu')
        self.tb.msg_connect(blk_pdu2ev, blk_pdu2ev.ports_out[0].port,
                            blk_snk, blk_snk.ports_in[0].port)

        #self.tb.run()  # for flowgraphs that will stop on its own!
        self.tb.start() 
        #mutex_prt(self.tb.msg_edge_list())
        #print tb.dump()
        time.sleep(6)     # to allow for Message source to finish
        self.tb.stop()
        self.tb.wait()

        return


if __name__ == '__main__':
    gr_unittest.run(qa_pdu_to_ev)


