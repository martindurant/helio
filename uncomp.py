import fsspec
from astropy.io import fits

fs = fsspec.filesystem("file")
allfiles = fs.ls("raw")

for i, afile in enumerate(allfiles):
    print(i, "/", len(allfiles) - 1)
    try:
        fs2 = fsspec.filesystem("tar", fo=afile)
        fitsfiles = fs2.glob("jsoc/*.fits")
        for fitsfile in fitsfiles:
            outfile = fitsfile.replace("jsoc/", "uncomp/")
            outfile = outfile.replace(":", "_")
            if fs.exists(outfile):
                continue
            with fs2.open(fitsfile, "rb") as f:
                hdul = fits.open(f)
                # .header is the on-the-fly apparent header, as opposed to
                # ._header, the original
                im = fits.ImageHDU(data=hdul[1].data, header=hdul[1].header)
                im.writeto(outfile, output_verify="silentfix", overwrite=True)
            print(fitsfile, "->", outfile)
        print("###", afile)
    except:
        print("###ERROR", afile)
