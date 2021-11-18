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
An ARQ Stop and Wait sender, witn an FSM.
'''

from gnuradio import gr

# GWN imports
from libgwn.gwnblock_py import gwnblock_py        # for all GWN blocks
from libgwn.gwnblock_py import mutex_prt          # for tests
from libgwn.fsm.gwnfsm import FSM, ExceptionFSM
from collections import deque

import pmt


###
### FSM definition
###


### Actions

def fn_send(fsm, event, block):
    '''Stores event to wait for ACK, sends event, starts timeout.'''
    fsm.dc['ev_to_ack'] = event       # event to wait for ACK
    fsm.dc['retries'] = 0             # event sent for first time, no retries yet
    block.timeouts[0].start()         # starts timeout to wait for ACK
    if fsm.debug:
        mutex_prt("    fn_send, ev_to_ack: " + str(fsm.dc['ev_to_ack']) )
        #fsm.print_state(['transition'])
        #msg = fsm.mesg_state(["state", "transition", "memory"])
        #mutex_prt(msg)
    block.process_data(event, 'Transmit')   # passes to block for transmission
    return

def fn_ack_ok(fsm, event, block):
    '''ACK received is correct, stop timeout.'''
    if event['seq_nr'] == fsm.dc['ev_to_ack']['seq_nr']:  # ACK is waited ACK 
        #fsm.dc['ev_to_ack'] = None   # no event to wait for
        block.timeouts[0].cancel()    # stops timeout waiting for ACK
        #fsm.dc['retries'] = 0        # set retries to 0 for next event
    else:                             # ACK is not the one expected
        pass                            
    return
    
def fn_sendfrombuffer(fsm, event, block):
    fsm.dc['ev_to_ack'] = fsm.mem.popleft()   # event to wait for ACK
    fsm.dc['retries'] = 0             # first time, no retries yet 
    fsm.dc['mem_nr_in'] -= 1          # one event less in buffer
    fsm.command = "Transmit"          # to output message
    if fsm.debug:
        mutex_prt("    fn_sendfrombuffer, ev_to_ack:" + str(fsm.dc['ev_to_ack']) + 
          ', buffer space: ' + str(fsm.dc['mem_max_len'] - fsm.dc['mem_nr_in']) )
    block.process_data(fsm.dc['ev_to_ack'], 'Transmit')   # for transmission
    return
    
def fn_resend(fsm, event, block):
    # ack_waited remains True
    fsm.dc['retries'] += 1            # increment retries
    fsm.command = "Transmit"          # to output message
    block.timeouts[0].start()         # starts timeout to wait for ACK
    if fsm.debug:
        mutex_prt("    fn_resend, FSM ev_to_ack:" + str(fsm.dc['ev_to_ack']) +
          ', retries left: ' + str(fsm.dc['max_retries'] - fsm.dc['retries']) ) 
    block.process_data(fsm.dc['ev_to_ack'], 'Transmit')   # for transmission
    return
    
def fn_push(fsm, event, block):
    fsm.mem.append(event)
    fsm.dc['mem_nr_in'] += 1
    if fsm.debug:
        mutex_prt("    fn_push, memory:" + str(fsm.mem) +
          ', buffer space: ' + str(fsm.dc['mem_max_len'] - fsm.dc['mem_nr_in']) )

def fn_stop(fsm, event, block):
    #if len(fsm.mem) > fsm.dc['mem_max_len']:
    if cn_buffer_full(fsm, event, block):
        command = "StopBufferFull"    # abort execution
    elif cn_no_retries_left(fsm, event, block):  
        command = "StopNoRetriesLeft"
    else:
        command = "StopOther"
    block.process_data(event, command)
    return


### Stop and Wait conditions


def cn_buffer_empty(fsm, event, block):
    if fsm.dc['mem_nr_in'] == 0:
        return True
    else: 
        return False
      
def cn_not_buffer_empty(fsm, event, block):
    #return not cn_buffer_empty(fsm, event, block)  # to avoid repeated messages
    if fsm.dc['mem_nr_in'] == 0: 
        return False
    else:                          # message in buffer
        return True
    
def cn_buffer_full(fsm, event, block):
    if fsm.dc['mem_nr_in'] >= fsm.dc['mem_max_len']: 
        return True
    else: 
        return False

def cn_not_buffer_full(fsm, event, block):
    if fsm.dc['mem_nr_in'] < fsm.dc['mem_max_len']: 
        return True
    else:
        return False

def cn_retries_left(fsm, event, block):
    if fsm.dc['retries'] < fsm.dc['max_retries']:
        return True
    else:
        return False

def cn_no_retries_left(fsm, event, block): 
    if fsm.dc['retries'] < fsm.dc['max_retries']:
        return False
    else:
        return True
    

### FSM generic action functions definitions

def fn_none(fsm, event, block):
    #fsm.action_result += "Result of function fn_none. "
    pass
    return

def fn_error(fsm, event, block):
    #fsm.mutex.lock()
    mutex_prt("  --- FSM error ")
    #fsm.action_result += "FSM ERROR"
    #fsm.mutex.unlock()
    return

def fn_init(fsm, event, block):
    #std::cout << "  --- FSM fn_init" << std::endl
    #fsm.action_result += "Result of function fn_init. "
    return

# FSM generic condition function definitions

def cn_True(fsm, event, block):
    return True

def cn_False(fsm, event, block):
    return False


### Stop and Wait States

def myfsm(p_dc={}, debug=False):
    '''Stop and Wait FSM.

    @param p_dc: a dictionary of values for the Stop and Wait protocol handling. It updates the default values with whatevers keys are given in argument.
    '''
    # dictionary of variables for Stop and Wait protocol handling
    dc = {}
    dc['Type'] = 'Data'       # event type to receive and transmit
    dc['Subtype'] = 'Data'    # event subtype to receive and transmit
    dc['AckType'] = 'Ctrl'    # ACK type waited for
    dc['AckStype'] = 'ACK'    # ACM subtype waited for
    dc['max_retries'] = 3     # max number of transmission retries
    dc['mem_max_len'] = 3     # max memory size, max number of events in queue

    dc.update(p_dc)           # updates keys given in parameter p_dc

    # these fields used as counters, not allowed to overwrite
    dc['retries'] = 0         # number of transmission retries executed so far
    dc['mem_nr_in'] = 0       # number of events in buffer
    dc['command'] = ''        # action to execute in block process_data function

    # FSM construction: initial state, memory as deque, dict of variables, debug
    deq = deque()
    f = FSM('Idle', mem=deq, dc=dc, debug=debug)
    
    # add ordinary transitions
    #f.add_transition(<input_symbol>, <state>, <action>, <next_state>, <condition>)
    #
    f.add_transition("Data", "Idle", fn_send, "WaitAck", None) #cn_True) 
    f.add_transition("CtrlAck", "WaitAck", fn_ack_ok, "Idle", cn_buffer_empty) 
    f.add_transition("CtrlAck", "WaitAck", fn_sendfrombuffer, "WaitAck",
        cn_not_buffer_empty)   
    f.add_transition("Timeout", "WaitAck", fn_resend, "WaitAck", cn_retries_left)
    f.add_transition("Data", "WaitAck", fn_push, "WaitAck", cn_not_buffer_full)
    f.add_transition("Data", "WaitAck", fn_stop, "Stop", cn_buffer_full) 
    f.add_transition("Timeout", "WaitAck", fn_stop, "Stop", cn_no_retries_left) 

    # default transition
    #f.add_transition ("", "", fn_error, "Idle", cn_True)
    f.set_default_transition (fn_error, "Idle")

    # transitions for any input symbol
    f.add_transition_any ("Idle", fn_none, "Idle", cn_True)
    f.add_transition_any ("Stop", fn_none, "Stop", cn_True)
    
    return f



###
###  Stop and Wait block
###


class stop_wait_send(gwnblock_py):
    '''An ARQ Stop and wait event sender.

    Receives an event, starts a timeout, writes this event on output port 1, and waits for an ACK to the message sent. On receiving the appropriate ACK, sends next message. On timeout, resends the unacknowledged message. Received messages are buffered in a FIFO list.
    @ivar ack_name: the name of the acknowledge event waited for.
    @ivar max_retries: number of times to resend event if ACK not received.
    @ivar tout_name: the name of the timer event waited for.
    @ivar timeout: the timeout in seconds.
    @ivar buffer_len: the buffer capacity, i.e. the maximum length of the list; 0  means no limit.
    @ivar debug: if True prints debug messages.
    @ivar fsm: a pointer to the Stop and Wait FSM.
    '''

    def __init__(self, ack_name='CtrlAck', max_retries=3, 
            tout_name='TimerACKTout', timeout=1.0, buffer_len=3, debug=False):
        '''Stop and Wait send constructor.

        @param ack_name: the name of the acknowledge event waited for.
        @param max_retries: number of times to resend event if ACK not received.
        @param tout_name: the name of the timer event waited for.
        @param timeout: the timeout in seconds.
        @param buffer_len: the buffer capacity, i.e. the maximum length of the list; 0  means no limit.
        @param debug: if True prints debug messages.
        '''
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
        self.fsm = myfsm(p_dc, debug=self.debug)

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


