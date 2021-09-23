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
A template for new GWN block creation in Python, QA.

This is the template for the new block QA code.
'''


from gnuradio import gr, gr_unittest
from gnuradio import blocks
from gwnblock_py import gwnblock_py
from virtual_channel import virtual_channel

# GWN imports
import pmt
import time
from gwnblock_py import mutex_prt     # for mutually exclusive printing


class qa_virtual_channel (gr_unittest.TestCase):
    '''
    QA for new GWN block in Python, created from template.
    '''
    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_virtual_channel(self):

        ### EXAMPLE CODE  
        #...
        #new_blk = virtual_channel(prob_loss=0.0,name="vchan")
        #...

        #self.tb.msg_connect( 
        #    (<emitter_block>, <out_port), 
        #    (<receiver_block>, <in_port>) )


        #self.tb.run()  # for flowgraphs that will stop on its own!
        self.tb.start() 
        #mutex_prt(self.tb.msg_edge_list())
        #print tb.dump()

        #time.sleep(8)

        self.tb.stop()
        self.tb.wait()

        return


if __name__ == '__main__':
    gr_unittest.run(qa_virtual_channel)


