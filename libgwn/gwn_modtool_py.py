#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
# Copyright 2015-2019
#   Instituto de Ingenieria Electrica, Facultad de Ingenieria,
#   Universidad de la Republica, Uruguay.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 
# 

import os   # to execute OS commands
import sys  # to capture parameters

import time

### adjust for your own use:
COPYRIGHT="'IIE FIng UdelaR'"
LICENSE_FILE="LICENSE"


### provide some help
HELP_MSG = \
"""
=== GWN new block creation script.
This script must be executed from the 'build' directory.
The following positional parameters may be given:
    <new_block_name> <nr_in> <nr_out> <nr_timers> <nr_timeouts>
These indicate the new block name, and the numbers of input ports, output ports, timers and timeouts.
If invoked with no positional parameters, the script will ask for them.
These parameters define the new block construction; they are not visible to block users. 
Next, the script will ask for the new block's own parameters, a list of Python parameters such as 
    msg_count, interval=100, payload="an example payload"
After confirmation, the script will create the new block, with all parameters included, for the programmer to customize.
===\n
"""

if "-h" in sys.argv or "--help" in sys.argv or "help" in sys.argv:
  print(HELP_MSG)
  sys.exit()


### execute script from build directory
CURDIR = os.popen("pwd").read()
#CURDIR = subprocess.run("pwd").read()
CURDIR = CURDIR.rstrip()          # strips whitespace, EOL
#print(CURDIR, len(CURDIR))        # for debug

if not CURDIR.endswith("build"):  # verify exec from ./build directory
  print("gwn_modtool_py:")
  print("  must be executed from the build directory")
  sys.exit()


### get values for gwnblock parameters 
# see if parameters provided in command line
if len (sys.argv) == 6:    # all parameters provided
  SCRIPT_NAME, BLOCK_NAME, NR_IN, NR_OUT, NR_TIMERS, NR_TIMEOUTS = sys.argv
else:                      # no parameters provided, ask for them
  print(HELP_MSG)
  print("\n...GWN block parameters:")
  BLOCK_NAME = input("   Block name: ")
  NR_IN = input("   Number of input ports: ")
  NR_OUT = input ("   Number of output ports: ")
  NR_TIMERS = input ("   Number of timers: ")
  NR_TIMEOUTS = input ("   Number of timeouts: ")
# create string list of gwnblock parameters
GWNBLOCK_PARS = "name='" + BLOCK_NAME + "', " 
GWNBLOCK_PARS += "number_in=" + NR_IN + ", " 
GWNBLOCK_PARS += "number_out=" + NR_OUT + ", " 
GWNBLOCK_PARS += "number_timers=" + NR_TIMERS + ", " 
GWNBLOCK_PARS += "number_timeouts=" + NR_TIMEOUTS 


### get values for new block own parameters
#BLOCK_PARS = input("    New block own parameter list: ")
BLOCK_PARS=""   # to correct, gr_modtool is not taking this


### confirm block creation
"""
print("... Ready to create new block, please verify:")
print("    New block name:", BLOCK_NAME)
print("    GWN block parameters:", GWNBLOCK_PARS)
print("    New block parameter list:", BLOCK_PARS)
ANSWER = "y"
ANSWER = input("Proceed (yY): ")
if ANSWER != "y" and ANSWER != "Y":
  print("    Answer was not 'y' nor 'Y'.")
  print("... gwn_modtool_py aborted, no new block created.")
  sys.exit()
"""

### create new GNU RAdio block with gr_modtool
#GR_MODTOOL = os.popen("which gr_modtool").read()

print("... gr_modtool: creating block " + BLOCK_NAME)
GR_MODTOOL_CMD = "cd ..; "
GR_MODTOOL_CMD += "gr_modtool add "
GR_MODTOOL_CMD += "--block-type sync --lang python --add-python-qa "
GR_MODTOOL_CMD += "--copyright " + COPYRIGHT + " --license-file " + LICENSE_FILE + " " + BLOCK_NAME + ";"
#GR_MODTOOL_CMD += "--argument-list " + BLOCK_PARS + " " + BLOCK_NAME + ";"
#GR_MODTOOL_CMD += BLOCK_NAME + "; "
GR_MODTOOL_CMD += "cd " + CURDIR + ";"
#GR_MODTOOL_CMD += " --argument-list=new_block_arglist 2>/dev/null; "
# stderr to /dev/null to avoid message of no identified consequence:
#   close failed in file object destructor:
#   sys.excepthook is missing
#   lost sys.stderr
print("gr_modtool command: " + GR_MODTOOL_CMD)    # for debug

try:
  # os.popen(GR_MODTOOL_CMD)
  ret_code = os.system(GR_MODTOOL_CMD)
  if ret_code != 0:
    print("... ERROR while executing gr_modtool")
    sys.exit()
  #print("... Waiting for gr_modtool to create new block.")
  #time.sleep(5)
  pass
except:
  print("... gr_modtool: an EXCEPTION occured.")
  print("... gwn_modtool_py aborted, no new block created.")
  sys.exit()
print("... gr_modtool: block " + BLOCK_NAME + " created.")

print("... Returning to build directory.")
os.popen("cd " + CURDIR)
#print("CURDIR", os.popen("pwd").read() )   # for debug

### copy new gwnblock template over new GR block created
FILE_NAME = "../python/" + BLOCK_NAME + ".py"
FILE_NAME_QA = "../python/qa_" + BLOCK_NAME + ".py"
print("... Copying new GWN block template into new block")
os.popen("cp ../libgwn/gwnblock_py_temp.py " + FILE_NAME)
os.popen("cp ../libgwn/gwnblock_py_temp_qa.py " + FILE_NAME_QA)

sys.exit()

### replace parameters in new block created
print("... Updating block name and parameters into new block code:")
print("       ", end=" "),
for fname in [FILE_NAME, FILE_NAME_QA]:
  print(fname, end=" ")
  f = open(fname, mode='r')
  block_code = f.read()
  f.close()
  block_code = block_code.replace("<BLOCK_NAME>", BLOCK_NAME)
  block_code = block_code.replace("<BLOCK_PARS>", BLOCK_PARS)
  block_code = block_code.replace("<GWNBLOCK_PARS>", GWNBLOCK_PARS)
  #print("\n=== Code for: " + fname + " ===")         #debug
  #print(block_code)                                  #debug
  #print("\n=== End code for: " + fname + " ===\n")   # debug
  # save modified code into new block files
  f = open(fname, mode='w')
  f.write(block_code)
  f.close()

print("\n... New block created.")
print("    To make available in GRC, please edit corresponding YAML file.")




