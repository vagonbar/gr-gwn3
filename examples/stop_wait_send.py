#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Stop and Wait send
# Author: Stop and Wait send example
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

from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import gwn3



from gnuradio import qtgui

class stop_wait_send(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Stop and Wait send ", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Stop and Wait send ")
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

        self.settings = Qt.QSettings("GNU Radio", "stop_wait_send")

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
        self.gwn3_virtual_channel_0 = gwn3.virtual_channel(0.5)
        self.gwn3_stop_wait_send_0 = gwn3.stop_wait_send('CtrlAck',5,'TimerACKTout',0.5,3,False)
        self.gwn3_stop_wait_ack_0 = gwn3.stop_wait_ack({'Type': 'Data', 'Subtype': 'Data'},{'Type': 'Ctrl', 'Subtype': 'ACK'},False)
        self.gwn3_msg_sink_1 = gwn3.msg_sink()
        self.gwn3_msg_sink_0 = gwn3.msg_sink()
        self.gwn3_event_source_0 = gwn3.event_source(10,1.0,{'Type': 'Data', 'Subtype': 'Data', 'seq_nr':0})



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.gwn3_event_source_0, 'out_0'), (self.gwn3_stop_wait_send_0, 'in_0'))
        self.msg_connect((self.gwn3_stop_wait_ack_0, 'out_0'), (self.gwn3_msg_sink_0, 'in_0'))
        self.msg_connect((self.gwn3_stop_wait_ack_0, 'out_1'), (self.gwn3_msg_sink_1, 'in_0'))
        self.msg_connect((self.gwn3_stop_wait_ack_0, 'out_1'), (self.gwn3_stop_wait_send_0, 'in_0'))
        self.msg_connect((self.gwn3_stop_wait_send_0, 'out_0'), (self.gwn3_virtual_channel_0, 'in_0'))
        self.msg_connect((self.gwn3_virtual_channel_0, 'out_0'), (self.gwn3_stop_wait_ack_0, 'in_0'))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "stop_wait_send")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate




def main(top_block_cls=stop_wait_send, options=None):

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
