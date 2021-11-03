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

'''A virtual channel block; receives and sends messages with probability loss.'''


from gnuradio import gr
from random import random

# GWN imports
from libgwn.gwnblock_py import gwnblock_py        # for all GWN blocks
from libgwn.gwnblock_py import mutex_prt          # for tests


class virtual_channel(gwnblock_py):
    '''Receives and resends a message with a probability loss.

    '''

    def __init__(self, prob_loss=0.0, debug=False):
      '''Virtual channel constructor.

      @param prob_loss: probability of not resending the received message.
      '''
      gwnblock_py.__init__(self, name='virtual_channel', number_in=1, number_out=1, number_timers=0, number_timeouts=0)
      self.prob_loss = float(prob_loss)
      self.debug = False     # True
      return


    def process_data(self, py_msg):
      '''Receives a message, outputs with probability loss.

      @param py_msg: message, a Python data type; GWN uses dict.
      '''
      rand_nr = random()
      
      if self.debug:
          dbg_msg = '--- Virtual Channel, prob_loss={0}; rand_nr={1}'.\
              format(self.prob_loss, rand_nr)
          mutex_prt(dbg_msg)
      if rand_nr <= self.prob_loss:
          pass					# no output
      else:
          self.write_out(py_msg)		# write event on output
      return

