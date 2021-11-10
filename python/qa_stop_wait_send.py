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


'''QA for stop_wait_send block.'''


from gnuradio import gr, gr_unittest
from gnuradio import blocks

from event_source import event_source
from stop_wait_send import stop_wait_send
from stop_wait_ack import stop_wait_ack
from virtual_channel import virtual_channel
from event_sink import event_sink

import pmt
import time
from libgwn.gwnblock_py import mutex_prt     # for mutually exclusive printing


class qa_stop_wait_send (gr_unittest.TestCase):
    '''QA for stop_wait_send block.
    '''
    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_stop_wait_send(self):

        ### blocks
        blk_src = event_source(10, 1.0, 
            {'Type':'Data', 'Subtype':'Data', 'seq_nr':0})
        blk_src.timers[0].debug = False     # True

        #p_dc = {'max_retries':5, 'mem_max_len':2}
        timeout = 0.8
        max_retries = 10
        buffer_len = 5
        blk_snd = stop_wait_send(timeout=timeout, max_retries=max_retries,
            buffer_len = buffer_len, debug=True)

        prob_loss = 0.8
        blk_vchan = virtual_channel(prob_loss)
        #blk_vchan.debug = True  # to see probability of loss

        ev_to_ack = {'Type':'Data', 'Subtype':'Data'}
        ack_to_send = {'Type':'Ctrl', 'Subtype':'ACK'}
        blk_ack = stop_wait_ack( ev_to_ack, ack_to_send, debug=False)

        blk_snk = event_sink(ev_count=True)

        ### connections
        self.tb.msg_connect( 
            (blk_src, blk_src.ports_out[0].port), 
            (blk_snd, blk_snd.ports_in[0].port) )
        self.tb.msg_connect(blk_snd, blk_snd.ports_out[0].port, 
            				blk_vchan, blk_vchan.ports_in[0].port )

        self.tb.msg_connect(blk_vchan, blk_vchan.ports_out[0].port, 
                            blk_ack, blk_ack.ports_in[0].port )
        self.tb.msg_connect(blk_ack, blk_ack.ports_out[0].port, 
                            blk_snk, blk_snk.ports_in[0].port)
        self.tb.msg_connect(blk_ack, blk_ack.ports_out[1].port, 
                            blk_snd, blk_snd.ports_in[0].port)

        ### run flowgraph
        #self.tb.run()  # for flowgraphs that will stop on its own!
        self.tb.start() 
        #mutex_prt(self.tb.msg_edge_list())
        #print tb.dump()
        time.sleep(30)      # time to allow for execution
        self.tb.stop()
        self.tb.wait()

        return


if __name__ == '__main__':
    gr_unittest.run(qa_stop_wait_send)


