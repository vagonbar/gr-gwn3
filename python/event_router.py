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

'''An event router block, outputs received event on one of two ports.'''


from gnuradio import gr

# GWN imports
from libgwn.gwnblock_py import gwnblock_py        # for all GWN blocks
from libgwn.gwnblock_py import mutex_prt          # for tests


class event_router(gwnblock_py):
    '''Outputs received event on port 0 or 1 according to event field values.

    Receives an event on its input port, sends this event on either output port 0 or output port 1, according to parameters field_nm_0, field_val_0, field_nm_1, field_val_1. An event which contains {field_nm_0:field_val_0} is sent on output port 0; an event with {field_nm_1:field_val_1} is sent on output port 1. If event does not meet any of those criteria, no event is sent on either output port.
    '''

    def __init__(self, field_nm_0,field_val_0,field_nm_1,field_val_1):
      '''Event router constructor.

      @param field_nm_0: field name 0, key of event dictionary.
      @param field_val_0: field value 0, value of field_mn_0 in event dictionary.
      @param field_nm_1: field name 1, key of event dictionary.
      @param field_val_1: field value 1, value of field_mn_1 in event dictionary.
      '''
      gwnblock_py.__init__(self, name='event_router', number_in=1, number_out=2, number_timers=0, number_timeouts=0)
      self.field_nm_0 = field_nm_0
      self.field_val_0 = field_val_0
      self.field_nm_1 = field_nm_1
      self.field_val_1 = field_val_1
      return


    def process_data(self, ev_rec):
      '''Outputs event on one of the two output ports.

      @param ev_rec: event received, a Python dictionary.
      '''
      if self.field_nm_0 in ev_rec and  \
          ev_rec[self.field_nm_0] == self.field_val_0:
        self.write_out(ev_rec, port_nr=0)
      elif self.field_nm_1 in ev_rec and  \
          ev_rec[self.field_nm_1] == self.field_val_1:
        self.write_out(ev_rec, port_nr=1)
      else:
        pass
      return

