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
   >>> img = sarprodata.astronaut()
   >>> top_left = img[:100, :100]

In order to change the shape of the image, :mod:`pysarpro.color` provides several
functions described in :ref:`sphx_glr_auto_examples_transform_plot_rescale.py`
.

.. literalinclude:: ../../examples/transform/plot_rescale.py
    :language: python
    :start-after: import matplotlib.pyplot as plt
    :end-before: fig, axes


.. image:: ../auto_examples/transform/images/sphx_glr_plot_rescale_001.png
   :target: ../auto_examples/transform/plot_rescale.html
   :align: center
   :width: 80%

Projective transforms (homographies)
------------------------------------

`Homographies <https://en.wikipedia.org/wiki/Homography>`_
are transformations of a Euclidean space that preserve the alignment of points.
Specific cases of homographies correspond to the conservation of more
properties, such as parallelism (affine transformation), shape (similar
transformation) or distances (Euclidean transformation). The different types
of homographies available in pysarpro are presented in
:ref:`sphx_glr_auto_examples_transform_plot_transform_types.py`.

Projective transformations can either be created using the explicit
parameters (e.g. scale, shear, rotation and translation)::

   import numpy as np
   import pysarpro as sarpro

   tform = sarprotransform.EuclideanTransform(
      rotation=np.pi / 12.,
      translation = (100, -20)
      )

or the full transformation matrix::

   matrix = np.array([[np.cos(np.pi/12), -np.sin(np.pi/12), 100],
                      [np.sin(np.pi/12), np.cos(np.pi/12), -20],
                      [0, 0, 1]])
   tform = sarprotransform.EuclideanTransform(matrix)

The transformation matrix of a transform is available as its ``tform.params``
attribute. Transformations can be composed by multiplying matrices with the
``@`` matrix multiplication operator.

Transformation matrices use
`Homogeneous coordinates <https://en.wikipedia.org/wiki/Homogeneous_coordinates>`_,
which are the extension of Cartesian coordinates used in Euclidean geometry to
the more general projective geometry. In particular, points at infinity can be
represented with finite coordinates.

Transformations can be applied to images using :func:`pysarpro.transform.warp`::

   img = sarproutil.img_as_float(sarprodata.chelsea())
   tf_img = sarprotransform.warp(img, tform.inverse)

.. image:: ../auto_examples/transform/images/sphx_glr_plot_transform_types_001.png
   :target: ../auto_examples/transform/plot_transform_types.html
   :align: center
   :width: 80%

The different transformations in :mod:`pysarpro.transform` have a ``estimate``
method in order to estimate the parameters of the transformation from two sets
of points (the source and the destination), as explained in the
:ref:`sphx_glr_auto_examples_transform_plot_geometric.py` tutorial::

   text = sarprodata.text()

   src = np.array([[0, 0], [0, 50], [300, 50], [300, 0]])
   dst = np.array([[155, 15], [65, 40], [260, 130], [360, 95]])

   tform3 = sarprotransform.ProjectiveTransform()
   tform3.estimate(src, dst)
   warped = sarprotransform.warp(text, tform3, output_shape=(50, 300))


.. image:: ../auto_examples/transform/images/sphx_glr_plot_geometric_002.png
   :target: ../auto_examples/transform/plot_geometric.html
   :align: center
   :width: 80%


The ``estimate`` method uses least-squares optimization to minimize the distance
between source and optimization.
Source and destination points can be determined manually, or using the
different methods for feature detection available in :mod:`pysarpro.feature`,
such as

 * :ref:`sphx_glr_auto_examples_features_detection_plot_corner.py`,
 * :ref:`sphx_glr_auto_examples_features_detection_plot_orb.py`,
 * :ref:`sphx_glr_auto_examples_features_detection_plot_brief.py`,
 * etc.

and matching points using :func:`pysarpro.feature.match_descriptors` before
estimating transformation parameters. However, spurious matches are often made,
and it is advisable to use the RANSAC algorithm (instead of simple
least-squares optimization) to improve the robustness to outliers, as explained
in :ref:`sphx_glr_auto_examples_transform_plot_matching.py`.

.. image:: ../auto_examples/transform/images/sphx_glr_plot_matching_001.png
   :target: ../auto_examples/transform/plot_matching.html
   :align: center
   :width: 80%

Examples showing applications of transformation estimation are

 * stereo matching
   :ref:`sphx_glr_auto_examples_transform_plot_fundamental_matrix.py` and
 * image rectification :ref:`sphx_glr_auto_examples_transform_plot_geometric.py`

The ``estimate`` method is point-based, that is, it uses only a set of points
from the source and destination images. For estimating translations (shifts),
it is also possible to use a *full-field* method using all pixels, based on
Fourier-space cross-correlation. This method is implemented by
:func:`pysarpro.registration.phase_cross_correlation` and explained in the
:ref:`sphx_glr_auto_examples_registration_plot_register_translation.py`
tutorial.

.. image:: ../auto_examples/registration/images/sphx_glr_plot_register_translation_001.png
   :target: ../auto_examples/registration/plot_register_translation.html
   :align: center
   :width: 80%


The
:ref:`sphx_glr_auto_examples_registration_plot_register_rotation.py` tutorial
explains a variant of this full-field method for estimating a rotation, by
using first a log-polar transformation.
