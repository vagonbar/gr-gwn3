from gnuradio import blocks
import pmt
from gnuradio import channels
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio import fec
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import gwn3

gwn3_packet_tx_gwn_0 = gwn3.packet_tx_gwn( 'digital.constellation_calcdist((digital.psk_2()[0]), (digital.psk_2()[1]), 2, 1).base()', 'fec.dummy_encoder_make(8000)', 'digital.header_format_default(digital.packet_utils.default_access_code, 0)', 'digital.constellation_calcdist((digital.psk_2()[0]), (digital.psk_2()[1]), 2, 1).base()', 'fec.dummy_encoder_make(8000)', [0,], 2)


