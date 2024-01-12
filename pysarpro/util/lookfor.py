import sys

import numpy as np


def lookfor(what):
    """Do a keyword search on pysarpro docstrings.

    Parameters
    ----------
    what : str
        Words to look for.

    Examples
    --------
    >>> import pysarpro
    >>> pysarpro.lookfor('regular_grid')  # doctest: +SKIP
    Search results for 'regular_grid'
    ---------------------------------
    pysarpro.lookfor
        Do a keyword search on pysarpro docstrings.
    pysarpro.util.regular_grid
        Find `n_points` regularly spaced along `ar_shape`.
    """
    return np.lookfor(what, sys.modules[__name__.split('.')[0]])
