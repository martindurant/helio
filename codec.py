import io

import numcodecs
from numcodecs.abc import Codec


class FITSCodec(Codec):
    codec_id = "fits_astropy"

    def __init__(self, ext=0):
        self.ext = ext

    def decode(self, buf, out=None):
        from astropy.io import fits
        b = io.BytesIO(buf)
        hdul = fits.open(b)
        hdu = hdul[self.ext]
        return hdu.data

    def encode(self, buf):
        raise NotImplementedError


numcodecs.register_codec(FITSCodec)
