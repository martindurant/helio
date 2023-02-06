import codec
from astropy.io import fits
import zarr
import fsspec
import kerchunk.fits
import kerchunk.utils


# original
im = fits.open("/media/mdurant/My Passport/SDO/raw/jsoc/aia.lev1.211A_2017-09-06T00_19_21.62Z.image_lev1.fits")[1].data


# single compressed array using astropy and whole files only to cope with compression
refs = {
  ".zarray": """{
    "zarr_format": 2,
    "shape": [4096, 4096],
    "chunks": [4096, 4096],
    "dtype": "int16",
    "filters": [
        {"id": "fits_astropy",
         "ext": 1}
    ],
    "fill_value": null,
    "compressor": null,
    "order": "C"
  }""",
  "0.0": ["/media/mdurant/My Passport/SDO/raw/jsoc/aia.lev1.211A_2017-09-06T00_19_21.62Z.image_lev1.fits"]
}

fs = fsspec.filesystem("reference", fo=refs)
z = zarr.open(fs.get_mapper())


# single uncompressed array with one chunk
url = "/media/mdurant/My Passport/SDO/uncomp/aia.lev1.211A_2017-09-06T00_19_21.62Z.image_lev1.fits"
refs = kerchunk.fits.FitsToZarr(url)

fs = fsspec.filesystem("reference", fo=refs)
z = zarr.open(fs.get_mapper())


# with 8 chunks
refs2 = kerchunk.utils.subchunk(refs, "1", 8)
fs2 = fsspec.filesystem("reference", fo=refs)
z2 = zarr.open(fs.get_mapper())


