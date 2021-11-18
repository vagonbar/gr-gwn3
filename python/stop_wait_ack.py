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


''' Stop and Wait ACK block.'''


from gnuradio import gr

# GWN imports
from libgwn.gwnblock_py import gwnblock_py        # for all GWN blocks
from libgwn.gwnblock_py import mutex_prt          # for tests



ev_to_ack={'Type':'Data', 'Subtype':'Data'}, 
'''Event received to acknowledge, a dictionary.'''
ack_to_send={'Type':'Ctrl', 'Subtype':'ACK'},
'''Event to send as ACK for event received, a dictionary.'''

class stop_wait_ack(gwnblock_py):
    '''Stop and Wait ACK block, sends ACK on expected event.

    @ivar ev_to_ack: a dictionary of fields to recognize events to acknowledge.
    @ivar ack_to_send: a dictionary of fields to generate ACK event to send back.
    @ivar debug: if True, prints debug messages.
    '''
    def __init__(self, 
            ev_to_ack={'Type':'Data', 'Subtype':'Data'}, 
            ack_to_send={'Type':'Ctrl', 'Subtype':'ACK'},
            debug=False):
      '''Stop and Wait ACK constructor.

      @param ev_to_ack: a dictionary of fields to recognize events to acknowledge.
      @param ack_to_send: a dictionary of fields to generate ACK event to send back.
      @param debug: if True, prints debug messages.
      '''
      gwnblock_py.__init__(self, name='stop_wait_ack', number_in=1, number_out=2, number_timers=0, number_timeouts=0)

      self.ev_to_ack = ev_to_ack
      self.ack_to_send = ack_to_send
      self.debug = debug

      return

    def process_data(self, event):
      '''Where message processing happens.

      Events to acknowledge must contain the (key, value) pairs in ev_to_ack. If event to acknowledge contains a field C{seq_nr}, the ACK event carries this number; if not, the ACK event returns C{{seq_nr:0}}.

      @param event: event received, a dictionary.
      '''
      # verify received event is the one to ACK:
      is_ev_to_ack = True
      for key in self.ev_to_ack.keys():
          if key in event and event[key] == self.ev_to_ack[key]:
              pass
          else:           # key to ACK not in event received
              is_ev_to_ack = False
              break  
      # send ACK or pass
      if is_ev_to_ack:
          if 'seq_nr' in event:
              self.ack_to_send['seq_nr'] = event['seq_nr']
          else:
              pass       # ACK with seq_nr=0 will be sent back
          if self.debug:
              msg_dbg = "--- stop_wait_ack, is_ev_to_ack: " + \
                str(is_ev_to_ack) + ", event: " + str(event) + \
                ", ACK to send: " + str(self.ev_to_ack)
              mutex_prt(msg_dbg)
          # send events
          self.write_out(self.ack_to_send, port_nr=1)
          self.write_out(event, port_nr=0)
      else:
          pass           # nothing done if event received is not event to ACK
      return

