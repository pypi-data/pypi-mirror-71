pims_nd2 : A reader for Nikon .ND2
==================================
[![build status](https://travis-ci.org/soft-matter/pims_nd2.png?branch=master)](https://travis-ci.org/soft-matter/pims_nd2)

`pims_nd2` contains a reader for nd2 files produced by NIS Elements. The reader is based on the included [SDK](http://www.nd2sdk.com) from Nikon, which makes it compatible with older versions of nd2 files. The reader is written in the [pims](https://github.com/soft-matter/pims) framework, enabling easy access to multidimensional files, lazy slicing, and nice display in IPython.

Installation
------------

`pims_nd2` is implemented on Windows, Linux and OSX systems. To obtain the latest stable version, install via PyPi:

    pip install pims_nd2

The ND2 SDK binaries are included in the package and will be copied into the `pims_nd2` package folder.

Dependencies
------------

This reader requires [pims](https://github.com/soft-matter/pims) version 0.3.0.

Examples
--------

The following code opens a movie file and displays a frame. Note that frames are only actually read when necessary:

    from pims import ND2_Reader
    frames = ND2_Reader('some_movie.nd2')
    frames[82]  # display frame 82
    frames.close()

The following code opens the multidimensional demo file included in the package and iterates through the first 3 frames. Note that we use a context manager here. We tell the reader which axis to iterate over and which axes to include in one frame. Also we select which channel to read.

    from pims import ND2_Reader
    with ND2_Reader('cluster.nd2') as frames:
		frames.iter_axes = 't'  # 't' is the default already
		frames.bundle_axes = 'zyx'  # when 'z' is available, this will be default
		frames.default_coords['c'] = 1  # 0 is the default setting
		for frame in frames[:3]:
			# do something with 3D frames in channel 1

The best way to use the reader is using a context manager. If you do not use a context manager, make sure to call `frames.close()` at the end of your script.

Metadata access can be done on two levels: reader level and frame level.

	frames.metadata['mpp']  # calibration in microns per pixel
	frames[0].metadata['t_ms']  # time of frame in milliseconds

Supporting Grant
----------------
This reader was developed by Casper van der Wel, as part of his PhD thesis work in Daniela Kraft's group at the Huygens-Kamerlingh-Onnes laboratory, Institute of Physics, Leiden University, The Netherlands. This work was supported by the Netherlands Organisation for Scientific Research (NWO/OCW).
