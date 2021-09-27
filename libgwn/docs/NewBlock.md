[GWN3, GNU Wireless Network 3](https://github.com/vagonbar/gr-gwn3)

## Creating a new GWN block

After cloning this repository, a new GWN block can be easily created using Python script ```gwn_modtool.py```. This script must be executed from the ```build``` subdirectory of your project.

The following positional parameters may be given:

```<new_block_name> <nr_in> <nr_out> <nr_timers> <nr_timeouts>```

These indicate the new block name, and the numbers of input ports, output ports, timers and timeouts. If invoked with no positional parameters, the script will ask for them. These parameters define the new block construction; they are not visible to block users. 

Next, the script will ask for the new block's own parameters, a list of Python parameters such as 

```msg_count, interval=100, payload="an example payload"```

Then the script will create the new block, with all parameters included, for the programmer to customize. This typically includes:


- in the new block python code, code initialization in constructor and code for processing in the ```process_data``` function.
- in the new block QA, inports for additional blocks, adjustment of parameters, and interconneting blocks in a flowgraph to test the new block capabilities.
- to make the new block available in GRC (GNU Radio Companion), adjustment of the corresponding YAML file in the ```grc``` subdirectory.

For example, the block msg_passer was created with the following commands:

```
cd build    # script must be executed from the build directory
../libgwn/gwn_modtool.py msg_passer 1 1 0 2
```

This indicates one input port, one output port, no timers, two timeouts. When the script asks for the blocks own parameters, the following was entered:

```tout_stop=5.0, tout_restart=8.0```

After confirmation, the script creates the new block through its files, with names and parameters as indicated by the user.

User defined behavior is then coded into the block, mainly by adapting the process_data function. The user defined parameters will be available in the constructor ```__init__```.

To make the new block available in GRC (GNU Radio Companion), the corresponding YAML file must be edited. The YAML file corresponding to the ```msg_passer``` block recently created may be found in ```grc/gwn3_msg_passer.block.yml```.

To make a pure Python blocks available as a module `in gwn3` package, it must be included in file `gr-gwn3/python/__init__.py` in a line like this:
```from .msg_passer import msg_passer```
After this, the usual `make; make install` command sequence completes the job.


[Back to README](../../README.md)
