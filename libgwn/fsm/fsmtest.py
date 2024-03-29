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

''' FSM for testing, tests transitions, functions, conditions.

A simple FSM to test transitions one by one, see if conditions enable a transition, and exec function.
'''


from libgwn.fsm.gwnfsm import FSM
from libgwn.fsm.gwnfsm import mutex_prt


### Actions


def fn_goA_1(fsm):
    mutex_prt('   FSM fn_goA_1; symbol ' + fsm.input_symbol)
    fsm.print_state(show=['action', 'transition'])
    return

def fn_goA_2(fsm):
    mutex_prt('   FSM fn_goA_2; symbol ' + fsm.input_symbol)
    fsm.print_state(show=['action', 'transition'])
    return

def fn_init(fsm):
    mutex_prt('   FSM fn_init; symbol ' + fsm.input_symbol)
    fsm.print_state(show=['action', 'transition'])
    return

def fn_error(fsm):
    mutex_prt('   FSM error')
    return

def fn_show(fsm):
    mutex_prt('   FSM fn_show; symbol ' + fsm.input_symbol )
    fsm.print_state(show=['action', 'transition'])
    return

def fn_none(fsm):
    mutex_prt('   FSM none')
    return

### Conditions

def cn_1_true(fsm):
    mutex_prt('   FSM cn_1_true')
    return True

def cn_2_true(fsm):
    mutex_prt('   FSM cn_2_true')
    return True

def cn_3_false(fsm):
    mutex_prt('   FSM cn_3_false')
    return False

def cn_4_false(fsm):
    mutex_prt('   FSM cn_4_false')
    return False


def myfsm():
    '''Definition of this particular FSM.

    @rtype: FSM object.
    @return: a pointer to an FSM object.
    '''
    f = FSM('INIT')

    f.set_default_transition(fn_error, 'INIT')
 
    # transitions for any input symbol
    f.add_transition_any ('INIT', fn_none, 'INIT')
    #f.add_transition_any ('State A', fn_none, 'State A')


    f.add_transition ('a1', 'INIT', fn_goA_1, 'State A', cn_1_true)
    f.add_transition ('i1', 'State A', fn_init, 'INIT', [cn_2_true])
    f.add_transition ('a2', 'INIT', fn_goA_1, 'State A', [cn_1_true, cn_2_true])
    f.add_transition ('i2', 'State A', fn_init, 'INIT', [cn_1_true, cn_2_true])
    f.add_transition ('a3', 'INIT', [fn_goA_1, fn_goA_2], 'State A', [cn_1_true])
    f.add_transition ('i3', 'State A', fn_init, 'INIT', '3 == 2')
    f.add_transition ('i4', 'State A', fn_init, 'INIT', [cn_3_false])

    print('GWN FSM test: print all transitions')
    f.print_state(show='state')

    return f


if __name__ == '__main__':
    print('=== GWN FSM test')
    print('    1. To test all transitions.')
    print('    2. To input one symbol at a time.')
    option = input('    Opción: ')
    f = myfsm()
    if option == '1':
        event = ['a1', 'i1', 'a2', 'i2', 'a3', 'i3', 'i4', 'i1']
        for ev in event:
            f.process(ev)
    else:
        try:
            event = 'j'
            while event:
                event = input('Event:')
                f.process(event)
        except KeyboardInterrupt as e: # Ctrl-C
            raise e



