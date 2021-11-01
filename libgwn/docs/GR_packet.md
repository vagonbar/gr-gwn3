[GWN3, GNU Wireless Network 3](https://github.com/vagonbar/gr-gwn3)

# GNU Radio packet blocks

Directory ```libgwn/GR_packet``` contains .py files generated from GR (GNU Radio) .grc files ```packet_tx.grc, packet_rx_grc y packet_loopback_hier.grc```. These .py files were modified by hand with some small corrections to make them run in GNU Radio 3.9.3.0.

The files were obtained by loading the .grc files in GRC (GNU Radio Companion), generating the flowgraphst (.py files), and then correcting these .py files. The .py files were stored by GRC in ~/.grc_gnuradio, and copied here to ensure they will not be inadvertently modified. 

From files packet_tx and packet_rx the following GWN blocks were created:
Parameter versions, all inputs and outputs, all parameters with default values, similar to original GR versions::
    ```
    packet_tx_gwn : Packet Tx GWN
    packet_tx_gwn : Packet Rx GWN
    ```

Modifications to these files::

    - constructor parameters with default value None; for each parameter, if arguent value is None, a default value is assigned. Default values assigned to all parameters ensure correct execution. Assigning to parameters default values obtained with calculations in de __init__ function resulted in some cases in segmentation fault errors. Hence, all parameters in __init__ function are assigned None values, and initialization occurs in the body of the __init__ function. The default values assigned were taken from the packet_loopback_hier.grc example flowgraph provided by GNU Radio.
    - once an argument value has been assigned to an atribute (self field), the attribute is used in all the class. This corrects the non recommended situation of using the parameter variable inside the constructor instead of the attribute to which this value had been asigned. E.g. use self.hdr_enc in rest of function instead of hdr_enc.
    - parameter eb added as such in packet_tx.


Original files in local /usr/share/gnuradio/examples/digital/packet/ ::
    ```
    - packet_tx.grc
    - packet_rx.grc
    - packet_loopback_hier.grc
    ```  

[Back to README](../../README.md)

