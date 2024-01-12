Getting started
---------------

``pysarpro`` is an image processing Python package that works with
:mod:`numpy` arrays. The package is imported as ``pysarpro``: ::

    >>> import pysarpro as sarpro

Most functions of ``pysarpro`` are found within submodules: ::

    >>> camera = sarpro.data.camera()

A list of submodules and functions is found on the `API reference
<https://pol-insar.github.io/docs/stable/api/api.html>`_ webpage.

Within pysarpro, images are represented as NumPy arrays, for
example 2-D arrays for grayscale 2-D images ::

    >>> type(camera)
    <type 'numpy.ndarray'>
    >>> # An image with 512 rows and 512 columns
    >>> camera.shape
    (512, 512)

The :mod:`pysarpro.data` submodule provides a set of functions returning
example images, that can be used to get started quickly on using
pysarpro's functions: ::

    >>> coins = sarpro.data.coins()
    >>> threshold_value = sarprofilters.threshold_otsu(coins)
    >>> threshold_value
    107

Of course, it is also possible to load your own images as NumPy arrays
from image files, using :func:`pysarpro.io.imread`: ::

    >>> import os
    >>> filename = os.path.join(sarpro.data_dir, 'moon.png')
    >>> moon = sarproio.imread(filename)

Use `natsort <https://pypi.org/project/natsort/>`_ to load multiple images ::

    >>> import os
    >>> from natsort import natsorted, ns
    >>> list_files = os.listdir('.')
    >>> list_files
    ['01.png', '010.png', '0101.png', '0190.png', '02.png']
    >>> list_files = natsorted(list_files)
    >>> list_files
    ['01.png', '02.png', '010.png', '0101.png', '0190.png']
    >>> image_list = []
    >>> for filename in list_files:
    ...   image_list.append(sarproio.imread(filename))
