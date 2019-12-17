# GGWN : GNU Wireless Network, version 3


GWN, the GNU Wireless Network, is a network development toolkit compatible with GNU Radio.

The main site of the project, [gr-gwncppvgb](https://github.com/vagonbar/gr-gwncppvgb) is developed both in Python and C++. GNU Radio imposes limitations on C++ inheritance, which makes development in C++ more difficult and involved. This is a significant drawback for using this toolkit in teaching and prototyping. In this site we are developing the project mainly in Python, specifically in Python 3, which will be de default in coming versions of GNU Radio.
The purpose of this site is then, twofold:
- to keep GWN simple to use and enhance with new user developed blocks.
- to bring the code to Python 3.

Please visit [gr-gwncppvgb](https://github.com/vagonbar/gr-gwncppvgb) for full documentation on the project.

Please consider this version as a work in progress.

## Installation

This version of GWN requires GNU Radio 3.8. The following instructions assume gr-gwn3 is cloned in the user's home directory under subdirectory GNURadio, and GNU Radio 3.8 is installed in /home/gnuradio-3.8.

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







