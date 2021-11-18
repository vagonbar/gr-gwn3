[GWN3, GNU Wireless Network 3](https://github.com/vagonbar/gr-gwn3)

# Installation

These notes offer some additional information on installation, as a complement to the [Quick Start page](QuickStart.md).

## GNU Radio

This version of GWN uses GNU Radio 3.9.  To install GNU Radio, plase see [InstallingGR](https://wiki.gnuradio.org/index.php/InstallingGR).

In Linux Mint 20, GNU Radio can be easily installed with the following commands:


```
  sudo add-apt-repository ppa:gnuradio/gnuradio-releases
  sudo apt-get update
  sudo apt-get install gnuradio
  gnuradio-companion -h   # shows installed version, e.g. 3.9.3.0
```

Some additional packages may be required:

```
  sudo apt install python3-distutils   # for GRC
  sudo apt install xterm               # instead of gnome-terminal
```

To install in a virtual machine, Linux Mint XFCE offers an Ubuntu based Linux installation with a light graphical environment, XFCE. 


## GWN

The following instructions assume `gr-gwn3` is cloned in the user's home directory under subdirectory `~/GNURadio`, and GNU Radio 3.8 is installed in `/home/gnuradio-3.8`. It also asumes `/home/gnuradio-3.8/setup_env.sh` has been sourced to make paths to GNU Radio available (command `source /home/gnuradio-3.8/setup_env.sh`, or its content has been included in the  `.bashrc` file.


```
  cd
  cd GNURadio/gr-gwn3
  rm -rf build; mkdir build      # only to get rid of old builds
  cd build
  cmake -DCMAKE_INSTALL_PREFIX=/home/gnuradio-3.8 ../
  make
  make install
  python3 ../python/qa_msg_passer.py 
```

The last command runs a test on an example flowgraph involving three blocks:

```  msg_source --> msg_passer --> msg_sink```

The source block emits messages at regular intervals, the passer block allows them to pass for some time, interrupts passing for another interval, then restarts passing messages to the sink block, which receives the messages and shows their content.
This very simple flowgraph shows handling of GWN messages as Python dictionaries (may by other structures), the use of input and output ports to send and receive messages, and the use of timers and timeouts to generate the messages and to interrupt or continue passing them. These are the main features of GWN, the handling of data messages and the use of time, a feature not present in GNU Radio.

This flowgraph is available in GRC by opening  `examples/msg_passer_test.grc`.

![Message passer example in GRC](../images/msg_passer_example.jpg)

To use GWN in GRC, you must ensure the PYTHONPATH environment variable contains the route to the GWN files, using a command such as:
```
  export PYTHONPATH=$PYTHONPATH:/home/GNURadio/gr-gwn3
```
This command may be included in your `.bashrc` file.


[Back to README](../../README.md)


