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


'''GWN3 new block creation script.

Creates a new GWN3 block with input ports, output ports, timers and timeouts according to given positional parameters, plus a list of user-defined parameters.
'''


import os   # to execute OS commands
import subprocess
import sys  # to capture parameters


### adjust for your own use:
COPYRIGHT="'IIE FIng UdelaR'"
'''Copyright holder.'''
LICENSE_FILE="LICENSE"
'''License file to include in blocks.'''

### verify current directory is 'build'
CURDIR = os.popen("pwd").read()
'''Current directory, must be the build directory.'''
#CURDIR = subprocess.run("pwd", capture_stdout=True).stdout
CURDIR = CURDIR.rstrip()          # strips whitespace, EOL
#print(CURDIR, len(CURDIR))        # for debug

BLOCK_NAME=""
'''New GWN block name.'''
GWNBLOCK_PARS=""
'''GWN block parameters, input ports, output ports, timers, timeouts.'''
BLOCK_PARS=""
'''User defined block parameters.'''
BLOCK_LABEL=""
'''Block label for GRC, to include in YAML file.'''


def show_help():
    '''Shows help for gwn_modtool script.'''
    HELP_MSG = \
    """
    GWN script for block creation and removal.
    This script must be executed from the 'build' directory.

    === To add a new GWN block::
        gwn_modtool add block_name> <nr_in> <nr_out> <nr_timers> <nr_timeouts>
    These indicate the new block name, and the numbers of input ports, output ports, timers and timeouts.
    If invoked with no positional parameters, the script will ask for them.
    These parameters define the new block construction; they are not visible to block users. 
    Next, the script will ask for the new block's own parameters, a list of Python parameters such as 
        msg_count, interval=100, payload="an example payload"
    Finally, the script asks for a block label for GRC inclusion.
    After confirmation, the script will create the new block, with all parameters included, for the programmer to customize.

    === To remove a GWN block::
        gwn_modtool rm <block_name>
    \n"""
    print(HELP_MSG)
    return


def verify_dir():
    '''Verifies script is run from build directory.'''
    # verify exec from ./build directory 
    if not CURDIR.endswith("build"):
        print("gwn_modtool:")
        print("  must be executed from the build directory")
        sys.exit()
    return


def get_pars(given_args, debug=False):
    '''Get parameters for block creation with gr_modtool.

    @param debug: if True prints new block GWN parameters and user parameters; default False.'''

    global BLOCK_NAME
    global GWNBLOCK_PARS
    global BLOCK_PARS
    global BLOCK_LABEL
    global CURDIR
    #print(given_args, len(given_args))
    #sys.exit()
    # see if parameters provided in command line
    if len (given_args) == 7:    # all parameters provided
        SCRIPT_NAME, CMD, BLOCK_NAME, NR_IN, NR_OUT, NR_TIMERS, NR_TIMEOUTS = \
            given_args
    else:                        # no parameters provided, ask for them
    #    show_help()  #print(HELP_MSG)
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
    BLOCK_PARS = input("    New block own parameter list: ")
    BLOCK_LABEL = input("    New block label for GRC: ")
    if debug:
        print("    BLOCK_NAME   :", BLOCK_NAME)
        print("    GWNBLOCK_PARS:", GWNBLOCK_PARS)
        print("    BLOCK_PARS   :", BLOCK_PARS)
    return


def create_block(debug=False):
    '''Creates blocks with parameters given using gr_modtool.

    @param debug: if True prints gr_modtool command and exit; if False executes gr_modtool command and creates GR block; default False.'''
    global BLOCK_NAME
    global GWNBLOCK_PARS
    global BLOCK_PARS
    
    ### confirm block creation
    #print("... Ready to create new block, please verify:")
    #print("    New block name:", BLOCK_NAME)
    #print("    GWN block parameters:", GWNBLOCK_PARS)
    #print("    New block parameter list:", BLOCK_PARS)
    #ANSWER = "y"
    #ANSWER = input("Proceed (yY): ")
    #if ANSWER != "y" and ANSWER != "Y":
    #  print("    Answer was not 'y' nor 'Y'.")
    #  print("... gwn_modtool aborted.")
    #  sys.exit()     # for debug

    ### create new GNU Radio block with gr_modtool
    print("... gr_modtool: creating block " + BLOCK_NAME)
    GR_MODTOOL_CMD = "cd ..; "
#   # echo necessary because asks for parameter list, even though given!
    GR_MODTOOL_CMD += "echo  | gr_modtool add "
    GR_MODTOOL_CMD += "--block-type sync --lang python --add-python-qa "
    GR_MODTOOL_CMD += " --copyright " + COPYRIGHT 
    GR_MODTOOL_CMD += " --license-file " + LICENSE_FILE 
    if BLOCK_PARS:
        GR_MODTOOL_CMD += " --argument-list " + BLOCK_PARS + " " 
    GR_MODTOOL_CMD += " --yes " + BLOCK_NAME
    print("    gr_modtool command: " + GR_MODTOOL_CMD)
    if debug:          # do not create block, just show command 
        print("    gr_modtool command: " + GR_MODTOOL_CMD)
        return
    try:
        ret_code = os.system(GR_MODTOOL_CMD)
        if ret_code != 0:
            print("... ERROR while executing gr_modtool")
            sys.exit()
    except:
        print("... gr_modtool: an EXCEPTION occured.")
        print("... gwn_modtool aborted, no new block created.")
        sys.exit()
    os.system("cd " + CURDIR)
    print("... gr_modtool: block " + BLOCK_NAME + " created.")
    #print("... Returning to build directory.")
    #os.popen("cd " + CURDIR)
    #print("CURDIR", os.popen("pwd").read() )   # for debug
    return


def copy_template(debug=False):
    '''Copy new gwnblock template, insert given parameters.
 
    @param debug: if True prints gwnblock template with inserted parameters; default False.'''

    global BLOCK_NAME
    global GWNBLOCK_PARS
    global BLOCK_PARS
    FILE_NAME = "../python/" + BLOCK_NAME + ".py"
    FILE_NAME_QA = "../python/qa_" + BLOCK_NAME + ".py"
    print("... Copying new GWN block template into new block")
    #os.popen not reliable! 
    #os.popen("cp ../libgwn/gwnblock_py_temp.py " + FILE_NAME)
    #os.popen("cp ../libgwn/gwnblock_py_temp_qa.py " + FILE_NAME_QA)
    subprocess.run(["cp", "../libgwn/gwnblock_py_temp.py", FILE_NAME])
    subprocess.run(["cp", "../libgwn/gwnblock_py_temp_qa.py", FILE_NAME_QA])
    #sys.exit()    # for debug

    ### replace parameters in new block created
    if debug:
        print("... Updating block name and parameters into new block code:")
        print("    block name:", BLOCK_NAME)
        print("    block pars:", BLOCK_PARS)
        print("    block init pars:", GWNBLOCK_PARS)
        print("    file names:", FILE_NAME, FILE_NAME_QA)
    for fname in [FILE_NAME, FILE_NAME_QA]:
        print("    ...updating " + fname)
        f = open(fname, mode='r')
        block_code = f.read()
        f.close()
        block_code = block_code.replace("<BLOCK_NAME>", BLOCK_NAME)
        block_code = block_code.replace("<BLOCK_PARS>", BLOCK_PARS)
        block_code = block_code.replace("<GWNBLOCK_PARS>", GWNBLOCK_PARS)
        if debug:
            print("\n=== Code for: " + fname + " ===")
            print(block_code)
            print("\n=== End code for: " + fname + " ===\n")
        else:
            # save modified code into new block files
            f = open(fname, mode='w')
            f.write(block_code)
            f.close()
    return


def copy_yaml(debug=False):
    '''Create YAML file for new block to make it available in GRC.

    @param debug: if True prints gr_modtool YAML command and exit; if False executes gr_modtool YAML command and creates YAML file for block; default False.'''

    global BLOCK_NAME
    global BLOCK_PARS
    global BLOCK_LABEL
    print("... Copying YAML template file")
    #subprocess.run(["cp", "../libgwn/gwnblock_py.block_temp.yml", 
    #    "../grc/gwn3_" + BLOCK_NAME + ".block.yml"])
    # read YAML template file
    f = open("../libgwn/gwnblock_py.block_temp.yml")
    block_code = f.read()
    f.close()
    # replace strings in lines of YANL template file
    print("... Updating block name and parameters into YAML file")
    block_code = block_code.replace("<BLOCK_NAME>", BLOCK_NAME)
    block_code = block_code.replace("<BLOCK_LABEL>", BLOCK_LABEL)
    par_list=""
    for par in BLOCK_PARS.split(","):
        par_list += "${" + par.split("=")[0] + "},"
    par_list = par_list[0:-1]
    block_code = block_code.replace("<BLOCK_PARS>", par_list)
    if debug:
        print(block_code)
        return
    # save customized template file as YAML file for this new block
    YAML_FNAME = "../grc/gwn3_" + BLOCK_NAME + ".block.yml"
    f = open(YAML_FNAME, mode='w')
    f.write(block_code)
    f.close()
    print("... gr_modtool: YAML file for block " + BLOCK_NAME + " created.")
    print("    To make available in GRC, please edit its YAML file.")
    return


def rm_block(debug=False):
    '''Removes block with gr_modtool.'''
    BLOCK_NAME = sys.argv[2]
    if sys.argv[1] != "rm":
        print("Error, to remove block: gwn_modtool rm block_name")
        return
    print("... gr_modtool: removing block " + BLOCK_NAME)
    GR_MODTOOL_CMD = "cd ..; "
    GR_MODTOOL_CMD += "gr_modtool rm " + BLOCK_NAME + " --yes;"
    GR_MODTOOL_CMD += "cd " + CURDIR + "; "
    if debug:
        print("... Removing block, command:")
        print("    ", GR_MODTOOL_CMD)
        return
    try:
        ret_code = os.system(GR_MODTOOL_CMD)
        if ret_code != 0:
            print("... ERROR while executing gr_modtool")
            sys.exit()
    except:
        print("... gr_modtool: an EXCEPTION occured.")
        print("... gwn_modtool aborted, block not removed.")
        sys.exit()
    print("... gr_modtool: block " + BLOCK_NAME + " removed.")


if __name__ == "__main__":

    #debug=True
    #print(sys.argv)
    #sys.exit()
    verify_dir()
    if sys.argv[1] == "add":            # add block  
        get_pars(sys.argv)
        create_block(False)
        #create_block(debug=True)
        copy_template()
        #copy_template(debug=True)
        copy_yaml()
        end_msg = "... New block created." + \
            "... Please include in python/__init__.py the line:" + \
            "\n        from \." + BLOCK_NAME + " import " + BLOCK_NAME + \
            "\n    for the new block to be included in the gwn3 package\n"
        print(end_msg)
    elif sys.argv[1] == "rm":           # remove block
        rm_block()
        #rm_block(True)
        sys.exit()
    else:                               # go on to create block
        #get_pars(sys.argv, True)
        show_help()
        sys.exit()




