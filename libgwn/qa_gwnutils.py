
#!/usr/bin/env python3
#-*- coding: utf-8 -*-
# 
# Copyright 2015-2021
#    Instituto de Ingenieria Electrica, Facultad de Ingenieria,
#    Universidad de la Republica, Uruguay.
#    https://iie.fing.edu.uy/
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




#import struct
#import numpy
#from gnuradio import gru
#import gwncrc as crc      # now included in this file

# for gwncrc
#from gnuradio.digital import digital_swig as digital
#import struct

import gwnutils

def test_make_packet(send_str):
        # values for encoding
        _samp_per_sym = 5
        _bits_per_sym = 2
        _preamble = gwnutils.default_preamble
        _access_code = gwnutils.default_access_code
        _pad_for_usrp = True
        _whitener_offset = False
        _whitening = True

        # frame packet
        send_pkt = gwnutils.make_packet(send_str,
            _samp_per_sym,
            _bits_per_sym,
            _preamble,
            _access_code,
            _pad_for_usrp,
            _whitener_offset,
            _whitening)

        print("=== make_packet:")
        print("    type: ", type(send_pkt))
        print(send_pkt)
        return send_pkt

if __name__ == "__main__":

    rec_pkt = test_make_packet("MESSAGE TO PACK")

    rec_str = gwnutils.unmake_packet(rec_pkt)
    print("=== unmake_packet:")
    print(rec_str)


