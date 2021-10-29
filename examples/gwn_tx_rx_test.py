#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: GWN Tx Rx test
# GNU Radio version: 3.9.3.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from gnuradio import blocks
from gnuradio import channels
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import gwn3



from gnuradio import qtgui

class gwn_tx_rx_test(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "GWN Tx Rx test", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("GWN Tx Rx test")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "gwn_tx_rx_test")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.gwn3_pdu_to_ev_0 = gwn3.pdu_to_ev()
        self.gwn3_packet_tx_gwn_0 = gwn3.packet_tx_gwn()
        self.gwn3_packet_rx_gwn_0 = gwn3.packet_rx_gwn()
        self.gwn3_event_source_0 = gwn3.event_source(10,1.0,{'Type':'Data', 'SubType':'Data', 'payload':'My payload'})
        self.gwn3_event_sink_0 = gwn3.event_sink(True)
        self.gwn3_ev_to_pdu_0 = gwn3.ev_to_pdu()
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=0.0,
            frequency_offset=0.0,
            epsilon=1.0,
            taps=[1.0],
            noise_seed=0,
            block_tags=True)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(1.0)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.gwn3_ev_to_pdu_0, 'pdu'), (self.gwn3_packet_tx_gwn_0, 'in'))
        self.msg_connect((self.gwn3_event_source_0, 'out_0'), (self.gwn3_ev_to_pdu_0, 'in_0'))
        self.msg_connect((self.gwn3_packet_rx_gwn_0, 'pkt out'), (self.gwn3_pdu_to_ev_0, 'pdu'))
        self.msg_connect((self.gwn3_pdu_to_ev_0, 'out_0'), (self.gwn3_event_sink_0, 'in_0'))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.gwn3_packet_rx_gwn_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.gwn3_packet_tx_gwn_0, 0), (self.channels_channel_model_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "gwn_tx_rx_test")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate




def main(top_block_cls=gwn_tx_rx_test, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
