#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2015-2021
#   Instituto de Ingenieria Electrica, Facultad de Ingenieria,
#   Universidad de la Republica, Uruguay.
#   https://iie.fing.edu.uy/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#

'''GWN version of GR packet_rx.
'''

from gnuradio import blocks
from gnuradio import digital
from gnuradio import fec
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from gnuradio.gr import types # for types byte_t, float_t
from gnuradio import pdu   # for pdu_to_tagged_stream, tagged_stream_to_pdu



class packet_rx_gwn(gr.hier_block2):
    ''' Packet transmission, receives PDU, codifies in stream and sends.

    Code adapted from GR packet_rx.py. Changes made:

      - after argument value assigned to attribute, use attribute instead of parameter in rest of code.
      - default arguments assigned to attributes; constructor can now be invoked with no arguments.
    '''
    #def __init__(self, eb=0.35, hdr_const=digital.constellation_calcdist((digital.psk_2()[0]), (digital.psk_2()[1]), 2, 1).base(), hdr_dec= fec.dummy_decoder.make(8000), hdr_format=digital.header_format_default(digital.packet_utils.default_access_code, 0), pld_const=digital.constellation_calcdist((digital.psk_2()[0]), (digital.psk_2()[1]), 2, 1).base(), pld_dec= fec.dummy_decoder.make(8000), psf_taps=[0,], sps=2):
    def __init__(self, eb=None, hdr_const=None, hdr_dec=None,
            hdr_format=None, pld_const=None, pld_dec=None, 
            psf_taps=None, sps=None):
        gr.hier_block2.__init__(
            self, "Packet Rx GWN",
                gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
                gr.io_signature.makev(5, 5, [gr.sizeof_gr_complex*1, gr.sizeof_gr_complex*1, gr.sizeof_gr_complex*1, gr.sizeof_gr_complex*1, gr.sizeof_gr_complex*1]),
        )
        self.message_port_register_hier_out("pkt out")
        self.message_port_register_hier_out("precrc")

        ##################################################
        # Parameters
        ##################################################
        if eb:
            self.eb = eb
        else:
            self.eb = 0.22
        if hdr_const:
            self.hdr_const = hdr_const
        else:
            self.hdr_const = Const_HDR = digital.constellation_calcdist( 
                digital.psk_2()[0], digital.psk_2()[1],
                2, 1, digital.constellation.AMPLITUDE_NORMALIZATION).base()
        if pld_const:
            self.pld_const = pld_const
        else:
            self.pld_const = Const_PLD = digital.constellation_calcdist(
                digital.psk_4()[0], digital.psk_4()[1],
                4, 1, digital.constellation.AMPLITUDE_NORMALIZATION).base()
        if hdr_format:
            self.hdr_format = hdr_format
        else:
            self.hdr_format = digital.header_format_counter( 
                digital.packet_utils.default_access_code, 3, 
                Const_PLD.bits_per_symbol() )
        if hdr_dec:
            self.hdr_dec = hdr_dec
        else:
            rep = 3
            self.hdr_dec = fec.repetition_decoder.make(
                self.hdr_format.header_nbits(),rep, 0.5)
        if pld_dec:
            self.pld_dec = pld_dec
        else:
            k = 7
            rate = 2
            polys = [109, 79]
            self.pld_dec = pld_dec = fec.cc_decoder.make(
                8000, k, rate, polys, 0, -1, fec.CC_TERMINATED, False)
        if sps:
            self.sps = sps
        else:
            self.sps = 2
        if psf_taps:
            self.psf_taps = psf_taps
        else:
            nfilts = 32
            self.psf_taps = rx_rrc_taps = firdes.root_raised_cosine(
            nfilts, nfilts*self.sps,1.0, self.eb, 11*self.sps*nfilts)


        ##################################################
        # Variables
        ##################################################
        self.preamble_rep = preamble_rep = [0xe3, 0x8f, 0xc0, 0xfc, 0x7f, 0xc7, 0xe3, 0x81, 0xc0, 0xff, 0x80, 0x38, 0xff, 0xf0, 0x38, 0xe0, 0x0f, 0xc0, 0x03, 0x80, 0x00, 0xff, 0xff, 0xc0]
        self.preamble_dummy = preamble_dummy = [0xac, 0xdd, 0xa4, 0xe2, 0xf2, 0x8c, 0x20, 0xfc]
        self.preamble_select = preamble_select = {1: preamble_dummy, 3: preamble_rep}
        self.rxmod = rxmod = digital.generic_mod(self.hdr_const, False, self.sps, True, self.eb, False, False)
        self.preamble = preamble = preamble_select[int(1.0/self.hdr_dec.rate())]
        self.mark_delays = mark_delays = [0, 0, 34, 56, 87, 119]
        self.nfilts = nfilts = 32
        self.modulated_sync_word = modulated_sync_word = digital.modulate_vector_bc(rxmod.to_basic_block(), preamble, [1])
        self.mark_delay = mark_delay = mark_delays[self.sps]

        ##################################################
        # Blocks
        ##################################################
        self.fec_generic_decoder_0 = fec.decoder(self.hdr_dec, gr.sizeof_float, gr.sizeof_char)
        self.fec_async_decoder_0 = fec.async_decoder(pld_dec, True, False, 1500*8)
        self.digital_protocol_parser_b_0 = digital.protocol_parser_b(self.hdr_format)
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(self.sps, 6.28/400.0, self.psf_taps, nfilts, nfilts/2, 1.5, 1)
        self.digital_header_payload_demux_0 = digital.header_payload_demux(
            (self.hdr_format.header_nbits() * int(1.0/self.hdr_dec.rate())) //  self.hdr_const.bits_per_symbol(),
            1,
            0,
            "payload symbols",
            "time_est",
            True,
            gr.sizeof_gr_complex,
            "rx_time",
            1.0,
            [],
            0)
        self.digital_crc32_async_bb_0 = digital.crc32_async_bb(True)
        self.digital_costas_loop_cc_0_0_0 = digital.costas_loop_cc(6.28/200.0, self.pld_const.arity(), False)
        self.digital_costas_loop_cc_0_0 = digital.costas_loop_cc(6.28/200.0, self.hdr_const.arity(), False)
        self.digital_corr_est_cc_0 = digital.corr_est_cc(modulated_sync_word, self.sps, mark_delay, 0.999, digital.THRESHOLD_ABSOLUTE)
        self.digital_constellation_soft_decoder_cf_0_0 = digital.constellation_soft_decoder_cf(self.hdr_const)
        self.digital_constellation_soft_decoder_cf_0 = digital.constellation_soft_decoder_cf(self.pld_const)
        self.blocks_tagged_stream_to_pdu_0 = pdu.tagged_stream_to_pdu(types.float_t, "payload symbols")
        self.blocks_tagged_stream_multiply_length_0 = blocks.tagged_stream_multiply_length(gr.sizeof_float*1, "payload symbols", self.pld_const.bits_per_symbol())
        self.blocks_multiply_by_tag_value_cc_0 = blocks.multiply_by_tag_value_cc("amp_est", 1)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self.fec_async_decoder_0, 'in'))
        self.msg_connect((self.digital_crc32_async_bb_0, 'out'), (self, 'pkt out'))
        self.msg_connect((self.digital_protocol_parser_b_0, 'info'), (self.digital_header_payload_demux_0, 'header_data'))
        self.msg_connect((self.fec_async_decoder_0, 'out'), (self.digital_crc32_async_bb_0, 'in'))
        self.msg_connect((self.fec_async_decoder_0, 'out'), (self, 'precrc'))
        self.connect((self.blocks_multiply_by_tag_value_cc_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.blocks_tagged_stream_multiply_length_0, 0), (self.blocks_tagged_stream_to_pdu_0, 0))
        self.connect((self.digital_constellation_soft_decoder_cf_0, 0), (self.blocks_tagged_stream_multiply_length_0, 0))
        self.connect((self.digital_constellation_soft_decoder_cf_0_0, 0), (self.fec_generic_decoder_0, 0))
        self.connect((self.digital_corr_est_cc_0, 0), (self.blocks_multiply_by_tag_value_cc_0, 0))
        self.connect((self.digital_corr_est_cc_0, 1), (self, 4))
        self.connect((self.digital_costas_loop_cc_0_0, 0), (self.digital_constellation_soft_decoder_cf_0_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0_0, 0), (self.digital_constellation_soft_decoder_cf_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0_0, 0), (self, 2))
        self.connect((self.digital_header_payload_demux_0, 0), (self.digital_costas_loop_cc_0_0, 0))
        self.connect((self.digital_header_payload_demux_0, 1), (self.digital_costas_loop_cc_0_0_0, 0))
        self.connect((self.digital_header_payload_demux_0, 0), (self, 0))
        self.connect((self.digital_header_payload_demux_0, 1), (self, 1))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_header_payload_demux_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self, 3))
        self.connect((self.fec_generic_decoder_0, 0), (self.digital_protocol_parser_b_0, 0))
        self.connect((self, 0), (self.digital_corr_est_cc_0, 0))


    def get_eb(self):
        return self.eb

    def set_eb(self, eb):
        self.eb = eb
        self.set_rxmod(digital.generic_mod(self.hdr_const, False, self.sps, True, self.eb, False, False))

    def get_hdr_const(self):
        return self.hdr_const

    def set_hdr_const(self, hdr_const):
        self.hdr_const = hdr_const
        self.set_rxmod(digital.generic_mod(self.hdr_const, False, self.sps, True, self.eb, False, False))

    def get_hdr_dec(self):
        return self.hdr_dec

    def set_hdr_dec(self, hdr_dec):
        self.hdr_dec = hdr_dec

    def get_hdr_format(self):
        return self.hdr_format

    def set_hdr_format(self, hdr_format):
        self.hdr_format = hdr_format

    def get_pld_const(self):
        return self.pld_const

    def set_pld_const(self, pld_const):
        self.pld_const = pld_const

    def get_pld_dec(self):
        return self.pld_dec

    def set_pld_dec(self, pld_dec):
        self.pld_dec = pld_dec

    def get_psf_taps(self):
        return self.psf_taps

    def set_psf_taps(self, psf_taps):
        self.psf_taps = psf_taps
        self.digital_pfb_clock_sync_xxx_0.update_taps(self.psf_taps)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_mark_delay(self.mark_delays[self.sps])
        self.set_rxmod(digital.generic_mod(self.hdr_const, False, self.sps, True, self.eb, False, False))

    def get_preamble_rep(self):
        return self.preamble_rep

    def set_preamble_rep(self, preamble_rep):
        self.preamble_rep = preamble_rep
        self.set_preamble_select({1: self.preamble_dummy, 3: self.preamble_rep})

    def get_preamble_dummy(self):
        return self.preamble_dummy

    def set_preamble_dummy(self, preamble_dummy):
        self.preamble_dummy = preamble_dummy
        self.set_preamble_select({1: self.preamble_dummy, 3: self.preamble_rep})

    def get_preamble_select(self):
        return self.preamble_select

    def set_preamble_select(self, preamble_select):
        self.preamble_select = preamble_select
        self.set_preamble(self.preamble_select[int(1.0/self.hdr_dec.rate())])

    def get_rxmod(self):
        return self.rxmod

    def set_rxmod(self, rxmod):
        self.rxmod = rxmod

    def get_preamble(self):
        return self.preamble

    def set_preamble(self, preamble):
        self.preamble = preamble

    def get_mark_delays(self):
        return self.mark_delays

    def set_mark_delays(self, mark_delays):
        self.mark_delays = mark_delays
        self.set_mark_delay(self.mark_delays[self.sps])

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts

    def get_modulated_sync_word(self):
        return self.modulated_sync_word

    def set_modulated_sync_word(self, modulated_sync_word):
        self.modulated_sync_word = modulated_sync_word

    def get_mark_delay(self):
        return self.mark_delay

    def set_mark_delay(self, mark_delay):
        self.mark_delay = mark_delay
        self.digital_corr_est_cc_0.set_mark_delay(self.mark_delay)

