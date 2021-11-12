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
An ARQ Stop and Wait sender.
'''

from gnuradio import gr

# GWN imports
from libgwn.gwnblock_py import gwnblock_py        # for all GWN blocks
from libgwn.gwnblock_py import mutex_prt          # for tests

import pmt

from stop_wait_FSM import *



class stop_wait_send(gwnblock_py):
    '''An ARQ Stop and wait event sender.

    Receives an event, starts a timeout, writes this event on output port 1, and waits for an ACK to the message sent. On receiving the appropriate ACK, sends next message. On timeout, resends the unacknowledged message. Received messages are buffered in a FIFO list.
    @param ack_name: the name of the acknowledge event waited for.
    @param max_retries: number of times to resend event if ACK not received.
    @param tout_name: the name of the timer event waited for.
    @param timeout: the timeout in seconds.
    @param buffer_len: the buffer capacity, i.e. the maximum length of the list; 0  means no limit.
    '''

    def __init__(self, ack_name='CtrlAck', max_retries=3, 
            tout_name='TimerACKTout', timeout=1.0, buffer_len=3, debug=False):
        gwnblock_py.__init__(self, name='stop_wait_send', 
            number_in=1, number_out=1, number_timers=0, number_timeouts=1)

        ## set attributes

        self.ack_name = ack_name
        self.max_retries = max_retries
        self.tout_name = tout_name
        self.timeout = timeout
        self.buffer_len = buffer_len
        #self.ls_buffer = []      # length must be checked in process
        self.debug = debug

        # dictionary of values to pass on to the FSM
        p_dc = {}
        if max_retries:
            p_dc['max_retries'] = max_retries
        if buffer_len:
            p_dc['mem_max_len'] = buffer_len


        ## initialize timeout waiting for ACK, start in FSM
        self.timeouts[0].timeout = self.timeout
        #self.timeouts[0].start()

        # create FSM
        self.fsm = myfsm(p_dc, debug=True)

        return


    def process_data(self, event, command=None):
        '''Writes event, waits for ACK, retransmits.

        The received event is passed on to the process function of the FSM; actions in the FSM are provided with the received event and a reference to the present block, so that they can access this block's attributes and functions, in particular the write_out function to send events.
        @param ev: a received event, a dictionary.
        '''
        if self.debug:
            #dbg_msg = str(ev)
            dbg_msg = '--- {0}, Type: {1}, Subtype: {2}'. \
                format(self.name(), event['Type'], event['Subtype'])
            dbg_msg += "; command: " + str(command) 
            if event['Subtype'] == 'Data':
                dbg_msg += ', seq_nr: {0}'.format(event['seq_nr'])
            mutex_prt(dbg_msg)

        # if FSM stopped, do nothin, just return
        if self.fsm.current_state == 'Stop':
            return

        # handle event to FSM process functions
        if not command:              # event comes from input port
            if event['Type'] == 'Data' and event['Subtype'] == 'Data':
                self.fsm.process('Data', event=event, block=self)
            elif event['Type'] == 'Ctrl' and event['Subtype'] == 'ACK':
                self.fsm.process('CtrlAck', event=event, block=self)
            elif event['Type'] == 'Internal' and event['Subtype'] == 'Timeout':
                self.fsm.process('Timeout', event=event, block=self)
        elif command == 'Transmit':  # event comes from FSM to transmit
            self.write_out(event)
        elif 'Stop' in command:      # event comes from FSM, FSM has stopped
            mutex_prt('--- {0}, FSM stopped, command: {1}'. \
                format(self.name(), command) )

        return


