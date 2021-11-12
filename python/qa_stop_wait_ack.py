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


'''QA for stop_wait_ack block.'''


from gnuradio import gr, gr_unittest
from gnuradio import blocks
from stop_wait_ack import stop_wait_ack

from event_source import event_source
from event_sink import event_sink


# GWN imports
import pmt
import time
from libgwn.gwnblock_py import mutex_prt     # for mutually exclusive printing


class qa_stop_wait_ack (gr_unittest.TestCase):
    '''QA for stop_wait_ack block.
    '''
    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_stop_wait_ack(self):

        # blocks
        blk_src = event_source(ev_count=5, interval=1.0, 
            ev_dc={'Type':'Data', 'Subtype':'Data', 'seq_nr':0} ) 

        ev_to_ack = {'Type':'Data', 'Subtype':'Data'}
        ack_to_send = {'Type':'Ctrl', 'Subtype':'ACK'}
        blk_ack = stop_wait_ack( ev_to_ack, ack_to_send, debug=True)

        blk_sdat = event_sink(ev_count=True)
        blk_sack = event_sink(ev_count=True)

        # connections
        self.tb.msg_connect( (blk_src, 'out_0'), (blk_ack, 'in_0') )
        self.tb.msg_connect( (blk_ack, 'out_0'), (blk_sdat, 'in_0') )
        self.tb.msg_connect( (blk_ack, 'out_1'), (blk_sack, 'in_0') )

        #self.tb.run()  # for flowgraphs that will stop on its own!
        self.tb.start() 
        #mutex_prt(self.tb.msg_edge_list())
        #print tb.dump()

        time.sleep(5)

        self.tb.stop()
        self.tb.wait()

        return


if __name__ == '__main__':
    gr_unittest.run(qa_stop_wait_ack)


