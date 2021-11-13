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

import sys, os, traceback, optparse, time, string
# add path to gwnfsm, gwnblock in FSM
#sys.path += ['..', '../../../python/']
from libgwn.fsm.gwnfsm import FSM
from libgwn.fsm.gwnfsm import mutex_prt


### Actions

def fn_none(fsm):
    mutex_prt('--- FSM none, nothing done\n')
    return

def fn_goA(fsm):
    mutex_prt('--- FSM fn_goA; symbol ' + fsm.input_symbol)
    fsm.print_state(show=['action', 'transition'])
    return

def fn_goB(fsm):
    mutex_prt('--- FSM fn_goB; symbol ' + fsm.input_symbol)
    fsm.print_state(show=['action', 'transition'])
    return

def fn_init(fsm):
    mutex_prt('--- FSM fn_init; symbol ' + fsm.input_symbol)
    fsm.print_state(show=['action', 'transition'])
    return

def fn_chgtoC(fsm):
    if fsm.to_c == True:
        fsm.to_c = False
    else:
        fsm.to_c = True
    mutex_prt('--- FSM fn_toC; symbol ' + fsm.input_symbol + \
        '; to_c set to ' + str(fsm.to_c) )
    fsm.print_state(show=['action', 'transition'])

def fn_chgwhr(fsm):
    if fsm.where == 'A':
        fsm.where = 'B'
    elif fsm.where == 'B':
        fsm.where = 'C'
    else:
        fsm.where = 'A'
    mutex_prt('--- FSM fn_init; symbol ' + fsm.input_symbol + \
        '; where=' + fsm.where)
    fsm.print_state(show=['action', 'transition'])
    return

def fn_show(fsm):
    mutex_prt('--- FSM fn_show; symbol ' + fsm.input_symbol + \
        '; where=' + fsm.where + ', to_c=' + str(fsm.to_c) )
    fsm.print_state(show=['action', 'transition'])

def fn_error(fsm):
    fsm.print_state(show=['action', 'transition'])


### Condition functions

def cn_toc(fsm):
    return fsm.to_c


### States

def myfsm():
    f = FSM ('INIT')

    # initial conditions
    f.where = 'A'
    f.to_c = False
    f.debug = False

    f.set_default_transition (fn_error, 'INIT')

    # transitions for any input symbol
    f.add_transition_any ('INIT', None, 'INIT')
    f.add_transition_any ('State A', fn_none, 'State A')

    # add ordinary transitions
    f.add_transition ('s', 'INIT', fn_show, 'INIT', None)

    f.add_transition ('g', 'INIT', fn_goA, 'State A', "self.where=='A'")
    f.add_transition ('g', 'INIT', fn_goB, 'State B', "self.where=='B'")
    f.add_transition ('g', 'INIT', [fn_goA, fn_goB], 'State C', \
        ["self.where=='C'", cn_toc])
    f.add_transition ('r', 'State A', fn_init, 'INIT', None)
    f.add_transition ('r', 'State B', fn_init, 'INIT', None)
    f.add_transition ('r', 'State C', fn_init, 'INIT', None)

    f.add_transition ('w', 'INIT', fn_chgwhr, 'Chg Where', None)
    f.add_transition ('c', 'INIT', fn_chgtoC, 'Chg ToC', None)
    f.add_transition ('r', 'Chg Where', fn_init, 'INIT', None)
    f.add_transition ('r', 'Chg ToC', fn_init, 'INIT', None)


    mutex_prt("\n--- FSM created, show state")
    f.print_state(show='state')

    #inputevs = [] # list of input events
    #f.process_list(inputevs)
    event = 'j'
    while event:
        event = input('Event:')
        for ev in event:
            f.process(ev)
    return f


if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), usage=globals()['__doc__'], version='$Id$')
        parser.add_option ('-v', '--verbose', action='store_true', default=False, help='verbose output')
        (options, args) = parser.parse_args()
        if options.verbose: mutex_prt(time.asctime() )
        #mutex_prt()
        mutex_prt('=== FSM, Finite State Machine example ===')
        mutex_prt('Input events (symbols, characters).')
        mutex_prt('To test all functions at once, please input')
        mutex_prt('    jsjsgrgjrwrsgrwrsgrcrsgrs')
        mutex_prt('Some symbols produce no action, please see FSM diagram.')
        mutex_prt('To finish, press Enter without any symbol.')
        myfsm() #main()
        if options.verbose: mutex_prt(time.asctime() )
        if options.verbose: mutex_prt('TOTAL TIME IN MINUTES:',)
        if options.verbose: mutex_prt((time.time() - start_time) / 60.0 )
        sys.exit(0)
    except KeyboardInterrupt as e: # Ctrl-C
        raise e
    except SystemExit as e: # sys.exit()
        raise e
    except Exception as e:
        mutex_prt('ERROR, UNEXPECTED EXCEPTION')
        mutex_prt(str(e))
        traceback.print_exc()
        os._exit(1)


