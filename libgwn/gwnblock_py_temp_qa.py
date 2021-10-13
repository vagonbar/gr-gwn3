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


'''QA for <BLOCK_NAME> block.'''


from gnuradio import gr, gr_unittest
from gnuradio import blocks
from gwnblock_py import gwnblock_py
from <BLOCK_NAME> import <BLOCK_NAME>

# GWN imports
import pmt
import time
from gwnblock_py import mutex_prt     # for mutually exclusive printing


class qa_<BLOCK_NAME> (gr_unittest.TestCase):
    '''QA for <BLOCK_NAME> block.
    '''
    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_<BLOCK_NAME>(self):

        ### EXAMPLE CODE  
        #...
        #new_blk = <BLOCK_NAME>(<BLOCK_PARS>)
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
    gr_unittest.run(qa_<BLOCK_NAME>)


