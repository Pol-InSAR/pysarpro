"""SAR Processing for Python

``pysarpro`` (a.k.a. ``pysarpro``) is a collection of algorithms for SAR image
processing.

The main package of ``pysarpro`` only provides a few utilities for converting
between image data types; for most features, you need to import one of the
following subpackages:

Subpackages
-----------
data
    Test images and example data.
io
    Reading, saving, and displaying images and video.
util
    Generic utilities.

Utility Functions
-----------------
img_as_float
    Convert an image to floating point format, with values in [0, 1].
    Is similar to `img_as_float64`, but will not convert lower-precision
    floating point arrays to `float64`.
img_as_float32
    Convert an image to single-precision (32-bit) floating point format,
    with values in [0, 1].
img_as_float64
    Convert an image to double-precision (64-bit) floating point format,
    with values in [0, 1].
img_as_uint
    Convert an image to unsigned integer format, with values in [0, 65535].
img_as_int
    Convert an image to signed integer format, with values in [-32768, 32767].
img_as_ubyte
    Convert an image to unsigned byte format, with values in [0, 255].
img_as_bool
    Convert an image to boolean format, with values either True or False.
dtype_limits
    Return intensity limits, i.e. (min, max) tuple, of the image's dtype.

"""

__version__ = '0.1.2'

from ._shared.version_requirements import ensure_python_version

ensure_python_version((3, 8))

import lazy_loader as lazy

__getattr__, __lazy_dir__, _ = lazy.attach_stub(__name__, __file__)


def __dir__():
    return __lazy_dir__() + ['__version__']


# Logic for checking for improper install and importing while in the source
# tree when package has not been installed inplace.
# Code adapted from scikit-learn's __check_build module.
_INPLACE_MSG = """
It appears that you are importing a local pysarpro source tree. For
this, you need to have an inplace install. Maybe you are in the source
directory and you need to try from another location."""

_STANDARD_MSG = """
Your install of pysarpro appears to be broken.
Try re-installing the package following the instructions at:
https://pol-insar.github.io/docs/stable/user_guide/install.html"""


def _raise_build_error(e):
    # Raise a comprehensible error
    import os.path as osp

    local_dir = osp.split(__file__)[0]
    msg = _STANDARD_MSG
    if local_dir == "pysarpro":
        # Picking up the local install: this will work only if the
        # install is an 'inplace build'
        msg = _INPLACE_MSG
    raise ImportError(
        f"{e}\nIt seems that pysarpro has not been built correctly.\n{msg}"
    )


try:
    # This variable is injected in the __builtins__ by the build
    # process. It used to enable importing subpackages of pysarpro when
    # the binaries are not built
    __pysarpro_SETUP__
except NameError:
    __pysarpro_SETUP__ = False

if __pysarpro_SETUP__:
    import sys

    sys.stderr.write('Partial import of pysarpro during the build process.\n')
    # We are not importing the rest of the scikit during the build
    # process, as it may not be compiled yet
else:
    try:
        from ._shared import geometry

        del geometry
    except ImportError as e:
        _raise_build_error(e)

    # Legacy imports into the root namespace; not advertised in __all__
    from .data import data_dir
    from .util.dtype import (
        dtype_limits,
        img_as_bool,
        img_as_float,
        img_as_float32,
        img_as_float64,
        img_as_int,
        img_as_ubyte,
        img_as_uint,
    )
    from .util.lookfor import lookfor


if 'dev' in __version__:
    # Append last commit date and hash to dev version information, if available

    import os.path
    import subprocess

    try:
        p = subprocess.Popen(
            ['git', 'log', '-1', '--format="%h %aI"'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.path.dirname(__file__),
        )
    except FileNotFoundError:
        pass
    else:
        out, err = p.communicate()
        if p.returncode == 0:
            git_hash, git_date = (
                out.decode('utf-8')
                .strip()
                .replace('"', '')
                .split('T')[0]
                .replace('-', '')
                .split()
            )

            __version__ = '+'.join(
                [tag for tag in __version__.split('+') if not tag.startswith('git')]
            )
            __version__ += f'+git{git_date}.{git_hash}'

from pysarpro._shared.tester import PytestTester  # noqa: F401,W203

test = PytestTester(__name__)
del PytestTester
