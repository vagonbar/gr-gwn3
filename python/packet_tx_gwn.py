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

'''GWN version of GR packet_tx.
'''

from gnuradio import blocks
from gnuradio import digital
from gnuradio import fec
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from gnuradio.filter import pfb
from gnuradio.gr import types  # for types byte_t, float_t
from gnuradio import pdu    # for pdu_to_tagged_sream, tagged_stream_to_pdu


class packet_tx_gwn(gr.hier_block2):
    ''' Packet reception, receives stream, decodifies into PDU and sends.

    Code adapted from GR packet_tx.py. Changes made:

      - after argument value assigned to attribute, use attribute instead of parameter in rest of code.
      - default arguments assigned to attributes; constructor can now be invoked with no arguments.
    '''
    #def __init__(self, hdr_const=digital.constellation_calcdist((digital.psk_2()[0]), (digital.psk_2()[1]), 2, 1).base(), hdr_enc= fec.dummy_encoder_make(8000), hdr_format=digital.header_format_default(digital.packet_utils.default_access_code, 0), pld_const=digital.constellation_calcdist((digital.psk_2()[0]), (digital.psk_2()[1]), 2, 1).base(), pld_enc= fec.dummy_encoder_make(8000), psf_taps=[0,], sps=2):
    def __init__(self, eb=None, hdr_const=None, hdr_enc=None, hdr_format=None,
            pld_const=None, pld_enc=None, psf_taps=None, sps=None):
        gr.hier_block2.__init__(
            self, "Packet Tx GWN",
                gr.io_signature(0, 0, 0),
                gr.io_signaturev(3, 3, [gr.sizeof_gr_complex*1, gr.sizeof_gr_complex*1, gr.sizeof_gr_complex*1]),
        )
        self.message_port_register_hier_in("in")
        self.message_port_register_hier_out("postcrc")


        ##################################################
        # Parameters
        ##################################################
        """
        self.hdr_const = hdr_const
        self.hdr_enc = hdr_enc
        self.hdr_format = hdr_format
        self.pld_const = pld_const
        self.pld_enc = pld_enc
        self.psf_taps = psf_taps
        self.sps = sps
        """
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
        if hdr_enc:
            self.hdr_enc = hdr_enc
        else:
            rep = 3
            self.hdr_enc = fec.repetition_encoder_make(8000, rep)
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
        if pld_enc:
            self.pld_enc = pld_enc
        else:
            k = 7
            rate = 2
            polys = [109, 79]
            self.pld_enc = pld_enc = fec.cc_encoder_make(
                8000,k, rate, polys, 0, fec.CC_TERMINATED, False)
        if sps:
            self.sps = sps
        else:
            self.sps = 2
            nfilts = 32
            self.psf_taps = tx_rrc_taps = firdes.root_raised_cosine(
                nfilts, nfilts,1.0, self.eb, 11*self.sps*nfilts)


        ##################################################
        # Variables
        ##################################################
        self.nfilts = nfilts = 32
        self.taps_per_filt = taps_per_filt = len(self.psf_taps)/nfilts
        self.filt_delay = filt_delay = int(1+(taps_per_filt-1)//2)

        ##################################################
        # Blocks
        ##################################################
        self.pfb_arb_resampler_xxx_0 = pfb.arb_resampler_ccf(
            self.sps,
            taps=self.psf_taps,
            flt_size=nfilts)
        self.pfb_arb_resampler_xxx_0.declare_sample_delay(filt_delay)
        self.fec_async_encoder_0_0 = fec.async_encoder(self.hdr_enc, True, False, False, 1500)
        self.fec_async_encoder_0 = fec.async_encoder(self.pld_enc, True, False, False, 1500)
        self.digital_protocol_formatter_async_0 = digital.protocol_formatter_async(self.hdr_format)
        self.digital_map_bb_1_0 = digital.map_bb(self.pld_const.pre_diff_code())
        self.digital_map_bb_1 = digital.map_bb(self.hdr_const.pre_diff_code())
        self.digital_crc32_async_bb_1 = digital.crc32_async_bb(False)
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bc(self.pld_const.points(), 1)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc(self.hdr_const.points(), 1)
        self.digital_burst_shaper_xx_0 = digital.burst_shaper_cc(firdes.window(window.WIN_HANN, 20, 0), 0, filt_delay, True, 'packet_len')
        #self.digital_burst_shaper_xx_0.set_block_alias("burst_shaper_a")
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_gr_complex*1, 'packet_len', 0)
        self.blocks_tagged_stream_multiply_length_0 = blocks.tagged_stream_multiply_length(gr.sizeof_gr_complex*1, 'packet_len', self.sps)
        self.blocks_repack_bits_bb_0_0 = blocks.repack_bits_bb(8, self.pld_const.bits_per_symbol(), 'packet_len', False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(8, self.hdr_const.bits_per_symbol(), 'packet_len', False, gr.GR_MSB_FIRST)
        self.blocks_pdu_to_tagged_stream_0_0 = pdu.pdu_to_tagged_stream(types.byte_t, 'packet_len')
        self.blocks_pdu_to_tagged_stream_0 = pdu.pdu_to_tagged_stream(types.byte_t, 'packet_len')



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.digital_crc32_async_bb_1, 'out'), (self.fec_async_encoder_0, 'in'))
        self.msg_connect((self.digital_crc32_async_bb_1, 'out'), (self, 'postcrc'))
        self.msg_connect((self.digital_protocol_formatter_async_0, 'payload'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))
        self.msg_connect((self.digital_protocol_formatter_async_0, 'header'), (self.fec_async_encoder_0_0, 'in'))
        self.msg_connect((self.fec_async_encoder_0, 'out'), (self.digital_protocol_formatter_async_0, 'in'))
        self.msg_connect((self.fec_async_encoder_0_0, 'out'), (self.blocks_pdu_to_tagged_stream_0_0, 'pdus'))
        self.msg_connect((self, 'in'), (self.digital_crc32_async_bb_1, 'in'))
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.blocks_repack_bits_bb_0_0, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_map_bb_1, 0))
        self.connect((self.blocks_repack_bits_bb_0_0, 0), (self.digital_map_bb_1_0, 0))
        self.connect((self.blocks_tagged_stream_multiply_length_0, 0), (self, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.digital_burst_shaper_xx_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self, 1))
        self.connect((self.digital_burst_shaper_xx_0, 0), (self, 2))
        self.connect((self.digital_burst_shaper_xx_0, 0), (self.pfb_arb_resampler_xxx_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.digital_map_bb_1, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.digital_map_bb_1_0, 0), (self.digital_chunks_to_symbols_xx_0_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.blocks_tagged_stream_multiply_length_0, 0))


    def get_hdr_const(self):
        return self.hdr_const

    def set_hdr_const(self, hdr_const):
        self.hdr_const = hdr_const

    def get_hdr_enc(self):
        return self.hdr_enc

    def set_hdr_enc(self, hdr_enc):
        self.hdr_enc = hdr_enc

    def get_hdr_format(self):
        return self.hdr_format

    def set_hdr_format(self, hdr_format):
        self.hdr_format = hdr_format

    def get_pld_const(self):
        return self.pld_const

    def set_pld_const(self, pld_const):
        self.pld_const = pld_const

    def get_pld_enc(self):
        return self.pld_enc

    def set_pld_enc(self, pld_enc):
        self.pld_enc = pld_enc

    def get_psf_taps(self):
        return self.psf_taps

    def set_psf_taps(self, psf_taps):
        self.psf_taps = psf_taps
        self.set_taps_per_filt(len(self.psf_taps)/self.nfilts)
        self.pfb_arb_resampler_xxx_0.set_taps(self.psf_taps)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.blocks_tagged_stream_multiply_length_0.set_scalar(self.sps)
        self.pfb_arb_resampler_xxx_0.set_rate(self.sps)

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_taps_per_filt(len(self.psf_taps)/self.nfilts)

    def get_taps_per_filt(self):
        return self.taps_per_filt

    def set_taps_per_filt(self, taps_per_filt):
        self.taps_per_filt = taps_per_filt
        self.set_filt_delay(int(1+(self.taps_per_filt-1)//2))

    def get_filt_delay(self):
        return self.filt_delay

    def set_filt_delay(self, filt_delay):
        self.filt_delay = filt_delay

