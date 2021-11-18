[GWN3, GNU Wireless Network 3](https://github.com/vagonbar/gr-gwn3)

# GWN Standard blocks

This document provides a brief description of GWN standard modules, i.e. those currently available off-the-shelf, developed by the GWN team. These modules perform some common tasks in data networks, allowing for some elementary experimentation. However, the main object of the GWN project is to provide a toolkit to develop new blocks for specific tasks; these "standard" blocks are provided for teaching and as a startpoint for experimentation and research in data networks.

## Messages and events

Blocks interchange information in the form of messages, an umbrella term for differente data types in the form of a sequence of bytes. Messages are discrete pieces of data, in contrast with the continuous streams usual in wireless communications. In GNU Radio, messages can be included in PDUs (Protocol Data Units), which in turn can be coded into tagged streams for transmission. 

In data networks, information is usually structured in named fields, such as type, subtype, source address, destination adress, payload, length, sequence number and many others; these fields vary according to the data protocols and the purpose of the different messages. To account for the wide variety of data fields, GWN uses a Python dictionary as a support structure, allowing for the versatility required to satisfy very different needs. These pieces of information supported in Python dictionaries are called "events" in GWN. Though any fields in a dictionary can be used, GWN recommends the following basic types: Internal, Data, Control, Management. 

Internal types are messages generated within the block, In GWN, these are messages from timers and timeouts, with corresponding subtypes Timer and Timeout. 

Data, Control, and Management are usual categories in data networks, with subtypes according to the protocol used.

A list of suggested and usual fields follows:: 

  `type` = { Internal, Data, Control, Management } (not mandatory).

  `subtype` : according to type and protocol.

  `src_addr` : source address, format according to protocol.

  `dst_addr` : destination address, format according to protocol.

  `duration` : float, a lapse of time.

  `frm_pkt` : frame packet, bytes, a binary packed string.

  `frm_len` : int, frame length,

  `payload` : string, information to transmit.

  `port` : a port number, to identify port of origin, in Internal types.

  `retry` : boolean, or int for number of retries. 


## Demo blocks

These blocks show the use of input ports, output ports, internal timers and  internal timeouts, and how to access them within a block. Messages are GWN events created by a GWN timer.

### Message source, [`msg_source`](https://htmlpreview.github.io/?https://github.com/vagonbar/gr-gwn3/blob/master/libgwn/html/gr-gwn3.python.msg_source.html)

Emits a number of messages at certain intervals, with a payload. Message emitted is the GWN event created by a GWN timer: type Internal, subtype Timer.  Shows use of GWN timers.

### Message passer, [`msg_sink`](https://htmlpreview.github.io/?https://github.com/vagonbar/gr-gwn3/blob/master/libgwn/html/gr-gwn3.python.msg_sink.html)
 
Receives a message in its input port, sends this message on its output port. Sending is interrupted by a timeout, and restarted after another timeout. Shows use of GWN timeouts.

### Message sink, [`msg_passer`](https://htmlpreview.github.io/?https://github.com/vagonbar/gr-gwn3/blob/master/libgwn/html/gr-gwn3.python.msg_passer.html)

Receives messages and shows them. If message is a GWN event (a dictionary) all keys and values are printed.

### Examples

```examples/msg_passer_test.grc```



## Event and channel blocks

### Event source, [`ev_source`](https://htmlpreview.github.io/?https://github.com/vagonbar/gr-gwn3/blob/master/libgwn/html/gr-gwn3.python.ev_source.html)

Emits a number of user defined events (dictionaries) at certain intervals. Type, subtype and other fields included in the message are entirely defined by the user.

### Event sink, [`ev_sink`](https://htmlpreview.github.io/?https://github.com/vagonbar/gr-gwn3/blob/master/libgwn/html/gr-gwn3.python.ev_sink)
 
Receives messages (events or other Python data type) and prints them. Optionally counts messages received.

### Virtual channel, [`virtual_channel`](https://htmlpreview.github.io/?https://github.com/vagonbar/gr-gwn3/blob/master/libgwn/html/gr-gwn3.python.virtual_channel.html)

Receives a message (event or other Python data type) and retransmits with a user defined probability loss.

### Event router, [`event_router`](https://htmlpreview.github.io/?https://github.com/vagonbar/gr-gwn3/blob/master/libgwn/html/gr-gwn3.python.event_router.html)

Receives an event on its input port, sends event on either output port 0 or 1, according to parameters field_nm_0, field_val_0, field_nm_1, field_val_1. An event which contains {field_nm_0:field_val_0} is sent on output port 0; an event with {field_nm_1:field_val_1} is sent on output port 1. If event does not meet any of those criteria, no event is sent on either output port.

### Examples

```examples/virtual_channel_test.grc```

```exmples/ev_router_test.grc```


## Conversion blocks

### Event to PDU, [`ev_to_pdu`](https://htmlpreview.github.io/?https://github.com/vagonbar/gr-gwn3/blob/master/libgwn/html/gr-gwn3.python.ev_to_pdu.html)

Converts an event (string or dictionary) into a PDU (Protocol Data Unit).

### PDU to event, [pdu_to_ev`](https://htmlpreview.github.io/?https://github.com/vagonbar/gr-gwn3/blob/master/libgwn/html/gr-gwn3.python.pdu_to_ev.html)

Converta a PDU (Protocol Data Unit) into an event (string or dictionary).

### Examples

```examples/ev_to_pdu_test.grc``` 

```examples/pdu_to_ev_test.grc```


## Transmission and reception blocks

These blocks are adaptated from GR packet blocks, please see [GR packet blocks](GR_packet.md) for a description of changes made in GWN blocks from the original GR blocks.

### Transmission block, [`packet_tx_gwn`](https://htmlpreview.github.io/?https://github.com/vagonbar/gr-gwn3/blob/master/libgwn/html/gr-gwn3.python.packet_tx_gwn.html)
 

Receives a PDU on its input ```in``` port, emits a stream on its output ```out``` port for transmission through a suitable air transmission device or through a Channel Model block for demonstration and testing.

### Reception block, [`packet_rx_gwn`](https://htmlpreview.github.io/?https://github.com/vagonbar/gr-gwn3/blob/master/libgwn/html/gr-gwn3.python.packet_rx_gwn.html)
 

Receives on its input ```in``` port a stream from a suitable air reception device or from a Channel Model block, emits a PDU on its output ```pkt out``` port.

### Examples

```examples/gr_packet_loopback_hier.grc``` : the GR example ```packet_loopback_hier``` implemented with modified versions of GR ```packet_tx``` and GR ```packet_rx```; small corrections were required to make these blocks run in GNU Radio 3.9.3.

```examples/gwn_packet_tx_rx_test.grc``` : a simplified version of GR ```gr_packet_loopback_hier``` using GWN packet blocks, preserving graphic outputs.

```examples/gwn_msg_tx_rx_channel_test.grc``` : transmission and reception of a data packet using only GWN blocks, through a GR channel model block. This example is a startpoint to build appllications in GWN. Virtual Source and Virtual Sink GR blocks can be substituted for interface blocks to suitable air or cable transmission devices.


[Back to README](../../README.md)
