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

'''QA for virtual channel block.'''

from gnuradio import gr, gr_unittest
from gnuradio import blocks

from virtual_channel import virtual_channel
from msg_source import msg_source
from msg_sink import msg_sink

# GWN imports
from time import sleep
from libgwn.gwnblock_py import mutex_prt     # for mutually exclusive printing


class qa_virtual_channel (gr_unittest.TestCase):
    '''QA for virtual channel block.
    '''
    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def run_test(self, prob_loss):
        '''Timer Source to Virtual Channel to Event Sink, with loss.
        '''
        msg_count = 10   # number of messages to send 
        ### blocks Timer Source --> Virtual Channel --> Event Sink
        blk_src = msg_source(msg_count, interval=1.0)
        blk_src.timers[0].debug = False    # True

        blk_vchan = virtual_channel(prob_loss)
        #blk_vchan.debug = True  # to see probability of loss
        blk_snk = msg_sink()

        self.tb.msg_connect(blk_src, blk_src.ports_out[0].port, 
            				blk_vchan, blk_vchan.ports_in[0].port )
        self.tb.msg_connect(blk_vchan, blk_vchan.ports_out[0].port, 
                            blk_snk, blk_snk.ports_in[0].port)

        secs = 12
        mutex_prt('\n=== Testing with ' + str(prob_loss) + ' probability loss===')
        mutex_prt('--- sends %d messages, waits %d secs\n' % (msg_count, secs,))
        #self.tb.run()  # for flowgraphs that will stop on its own!
        self.tb.start() 
        #mutex_prt(self.tb.msg_edge_list())
        sleep(secs)

        blk_src.stop_timers()
        mutex_prt('--- sender, timers stopped')
        
        self.tb.stop()
        self.tb.wait()
        mutex_prt('--- top block stopped')
        
        return

    def test_1(self):
        '''Test with 0.5 prob loss.'''
        self.run_test(0.5)

    def test_no_loss(self):
        '''Test with 0.0 prob loss, no loss.'''
        self.run_test(0.0)

    def test_total_loss(self):
        '''Test with 1.0 prob loss, total loss.'''
        self.run_test(1.0)



if __name__ == '__main__':
    gr_unittest.run(qa_virtual_channel)


