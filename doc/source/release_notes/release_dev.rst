:orphan:

pysarpro 0.X.0 release notes
================================

pysarpro is an SAR processing library for the scientific Python
ecosystem that includes algorithms for segmentation, geometric
transformations, feature detection, registration, color space
manipulation, analysis, filtering, morphology, and more.

For more information, examples, and documentation, please visit our website:

https://pol-insar.github.io


New Features
------------

- Add parameters ``mode`` and ``cval`` to ``erosion``, ``dilation``, ``opening``, ``closing``, ``white_tophat``, and ``black_tophat`` in ``pysarpro.morphology``;
  add parameter ``mode`` to ``binary_erosion``, ``binary_dilation``, ``binary_opening`` and ``binary_closing`` in ``pysarpro.morphology``;
  add functions ``mirror_footprint`` and ``pad_footprint`` to ``pysarpro.morphology``;
  (`#6695 <https://github.com/Pol-InSAR/pysarpro/pull/6695>`_).

Improvements
------------



Bugfixes
--------

- ``pysarpro.morphology.closing`` and ``pysarpro.morphology.opening`` were not extensive and anti-extensive, respectively, if the footprint was not mirror symmetric
  (`#6695 <https://github.com/Pol-InSAR/pysarpro/pull/6695>`_).

Deprecations
------------

- Parameters ``shift_x`` and ``shift_y`` in ``pysarpro.morphology.erosion`` and ``pysarpro.morphology.dilation`` are deprecated and a warning is emitted if they are given.
  (`#6695 <https://github.com/Pol-InSAR/pysarpro/pull/6695>`_).

Contributors to this release
----------------------------
