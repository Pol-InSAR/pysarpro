============================================
Geometrical transformations of images
============================================

Cropping, resizing and rescaling images
---------------------------------------

.. currentmodule:: pysarpro.transform

Images being NumPy arrays (as described in the :ref:`numpy_images` section), cropping
an image can be done with simple slicing operations. Below we crop a 100x100
square corresponding to the top-left corner of the astronaut image. Note that
this operation is done for all color channels (the color dimension is the last,
third dimension)::

   >>> import pysarpro as sarpro
   >>> img = sarpro.data.astronaut()
   >>> top_left = img[:100, :100]
