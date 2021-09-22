# GWN3. Installation

This version of GWN requires GNU Radio 3.8. The following instructions assume gr-gwn3 is cloned in the user's home directory under subdirectory ```~/GNURadio```, and GNU Radio 3.8 is installed in ```/home/gnuradio-3.8```, and ```/home/gnuradio-3.8/setup_env.sh``` has been sourced to make paths to GNU Radio available (command ```source /home/gnuradio-3.8/setup_env.sh``` or included in ```.bashrc``` file).

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

This flowgraph is available in GRC by opening  ```examples/msg_passer_example.grc```.

![Message passer example in GRC](../images/msg_passer_example.jpg)


[Back to README](../../README.md)


