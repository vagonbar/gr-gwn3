[GWN3, GNU Wireless Network 3](https://github.com/vagonbar/gr-gwn3)

# GWN Standard blocks

This document provides a brief description of GWN standard modules, i.e. those currently available off-the-shelf, developed by the GWN team. These modules perform some common tasks in data networks, allowing for some elementary experimentation. However, the main object of the GWN project is to provide a toolkit to develop new blocks for specific tasks; these "standard" blocks are provided for teaching and as a startpoint for experimentation and research in data networks.

## Messages and events

Blocks interchange information in the form of messages, an umbrella term for differente data types in the form of a sequence of bytes. Messages are discrete pieces of data, in contrast with the continuous streams usual in wireless communications. In GNU Radio, messages can be included in PDUs (Protocol Data Units), which in turn can be coded into tagged streams for transmission. 

In data networks, information is usually structured in named fields, such as type, subtype, source address, destination adress, payload, length, sequence number and many others; these fields vary according to the data protocols and the purpose of the different messages. To account for the wide variety of data fields, GWN uses a Python dictionary as a support structure, allowing for the versatility required to satisfy very different needs. These pieces of information supported in Python dictionaries are called "events" in GWN. Though any fields in a dictionary can be used, GWN recommends the following basic types: Internal, Data, Control, Management. 

Internal types are messages generated within the block, In GWN, these are messages from timers and timeouts, with corresponding subtypes Timer and Timeout. 

Data, Control, and Management are usual categories in data networks, with subtypes according to the protocol used.

A list of suggested and usual fields follows:: 

  `type` = { Internal, Data, Control, Management }` (not mandatory).
  `subtype` : according to type and protocol.
  `src_addr` : source address, format according to protocol.
  `dst_addr` : destination address, format according to protocol.
  `duration` : float, a lapse of time.
  `frm_pkt : frame packet, bytes, a binary packed string.
  `frm_len` : int, frame length,
  `payload` : string, information to transmit.
  `port : a port number, to identify port of origin, in Internal types.
  `retry` : boolean, or int for number of retries DEFINE. 


## Demo blocks

These blocks show the use of input ports, output ports, internal timers and  internal timeouts, and how to access them within a block. Messages are GWN events created by a GWN timer.

### Message source, [`msg_source`](https://htmlpreview.github.io/?https://github.com/vagonbar/gr-gwn3/blob/master/libgwn/html/gr-gwn3.python.msg_source.html)

Emits a number of messages at certain intervals, with a payload. Message emitted is the GWN event created by a GWN timer: type Internal, subtype Timer.  Shows use of GWN timers.

### Message passer, [`msg_sink`](https://htmlpreview.github.io/?https://github.com/vagonbar/gr-gwn3/blob/master/libgwn/html/gr-gwn3.python.msg_sink.html)
 
Receives a message in its input port, sends this message on its output port. Sending is interrupted by a timeout, and restarted after another timeout. Shows use of GWN timouts.

### Message sink, [`msg_passer`](https://htmlpreview.github.io/?https://github.com/vagonbar/gr-gwn3/blob/master/libgwn/html/gr-gwn3.python.msg_passer.html)

Receives messages and shows them. If message is a GWN event (a dictionary) all keys and values are printed.


## Event and channel blocks

### Event source, `ev_source`

Emits a number of user defined events (dictionaries) at certain intervals. Type, subtype and other fields included in the message are entirely defined by the user.

### Event sink, `ev_sink`
Receives messages (events or other Python data type) and prints them. Optionally counts messages received.

### Virtual channel, `virtual_channel`

Receives a message (event or other Python data type) and retransmits with a user defined probability loss.

### Event router, `event_router`

Receives an event on its input port, sends event on either output port 0 or 1, according to parameters field_nm_0, field_val_0, field_nm_1, field_val_1. An event which contains {field_nm_0:field_val_0} is sent on output port 0; an event with {field_nm_1:field_val_1} is sent on output port 1. If event does not meet any of those criteria, no event is sent on either output port.

## Conversion blocks

### Event to PDU, `ev_to_pdu`

### PDU to event, `pdu_to_ev`

### PSK transmit, `hier_tx_psk`

### PSK receive, `hier_rx_psk`



## Framers

### L1 framer, `l1_framer`

### L1 deframer, `l1_deframer`



[Back to README](../../README.md)
