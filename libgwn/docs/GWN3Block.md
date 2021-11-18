[GWN3, GNU Wireless Network 3](https://github.com/vagonbar/gr-gwn3)

# GWN3 block characteristics


## GWN messages and ports

Each GWN block may contain 0, 1 or more input ports, and 0, 1 or more output ports. Input and output ports are message ports. A message is a GNU Radio PMT ([PolyMorphic data Type](https://wiki.gnuradio.org/index.php/Polymorphic_Types_(PMTs)). GNU Radio provides a very complete set of functions to convert to and from a number of data types into PMT data types.

Messages are just a PMT dictionary type. This allows the user to insert any data type identified by a name. GWN suggests to use Type and Subtype as keys in the message dictionary, since these pieces of information are commonly used in data networks. However, the user may interchange between her blocks messages of any PMT type.


## GWN Timers

A GWN timer is an object which can be attached to a block to emit internal messages periodically for a number of times. A timer can be given as parameters the message to emit, the period of time between messages, and the total number of messages to emit.

The block containing the timer receives messages from the timer in an internal input port. This internal port, called a timer port, is a message port of the block, but it is not connected to any external block. All timers in the block send their messages to this unique timer input port. 

When started, the timer waits for the indicated period of time before emitting its first message. Then, the timer goes on sending messages after each period of time, until reaching the number of messages indicated as a count parameter. Once the count has been reached, no more messages are sent. However, the timer thread is not finished, and can be restarted.

The timer can be suspended in its emission of messages. When suspended, the timer does not emit messages, and the counter is not incremented, but the timer thread remains alive. When taken out from suspension, messages continue to be emitted and the counter is incremented from its last value.

The timer can be stopped before reaching its assigned number of messages to emit. In this case, no messages are emitted any more, and the timer thread is terminated.The counter can be resetted, thus starting to emit messages as if it was recently started.

The message emmited by the timer is a GWN message, i.e. a port identifier and a dictionary in PMT format. In a GWN message, the dictionary contains a type, a subtype, and a sequence number, with the optional addition of other entries defined by the user. Each message is passed to the main block function `process_data`, where the actions defined by the programmer happen.


## GWN Timeouts

A GWN timeout is similar to a GWN timer but only one message is emitted after the configured time has elapsed. The timeout message is received by the `process_data` function for the user to act accordingly. A timeout object can be interrupted before its action starts, i.e. before it sends its message.


[Back to README](../../README.md)


