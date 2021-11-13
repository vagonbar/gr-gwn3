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


''' FSM for testing, tests (tries to) all features.
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
    f = FSM('INIT')

    f.set_default_transition(fn_error, 'INIT')
 
    # transitions for any input symbol
    f.add_transition_any ('INIT', fn_none, 'INIT')
    #f.add_transition_any ('State A', fn_none, 'State A')


    f.add_transition ('a', 'INIT', fn_goA_1, 'State A', cn_1_true)
    f.add_transition ('b', 'State A', fn_init, 'INIT', [cn_2_true])
    f.add_transition ('c', 'INIT', fn_goA_1, 'State A', [cn_1_true, cn_2_true])
    f.add_transition ('d', 'State A', fn_init, 'INIT', [cn_1_true, cn_2_true])
    f.add_transition ('e', 'INIT', [fn_goA_1, fn_goA_2], 'State A', [cn_1_true])
    f.add_transition ('z', 'State A', fn_init, 'INIT', [cn_2_true])

    event = 'j'
    while event:
        event = input('Event:')
        for ev in event:
            f.process(ev)
    return f


if __name__ == '__main__':
    try:
        myfsm()
    except KeyboardInterrupt as e: # Ctrl-C
        raise e



