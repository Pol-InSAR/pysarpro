import pathlib
from tempfile import NamedTemporaryFile

import numpy as np
import pytest
from numpy.testing import assert_array_equal

from pysarpro.io import imread, imsave, reset_plugins, use_plugin


def setup():
    use_plugin('tifffile')
    np.random.seed(0)


def teardown():
    reset_plugins()


class TestSave:
    def roundtrip(self, dtype, x, use_pathlib=False, **kwargs):
        with NamedTemporaryFile(suffix='.tif') as f:
            fname = f.name

        if use_pathlib:
            fname = pathlib.Path(fname)
        imsave(fname, x, check_contrast=False, **kwargs)
        y = imread(fname)
        assert_array_equal(x, y)

    shapes = ((10, 10), (10, 10, 3), (10, 10, 4))
    dtypes = (np.uint8, np.uint16, np.float32, np.int16, np.float64)

    @pytest.mark.parametrize("shape", shapes)
    @pytest.mark.parametrize("dtype", dtypes)
    @pytest.mark.parametrize("use_pathlib", [False, True])
    @pytest.mark.parametrize('explicit_photometric_kwarg', [False, True])
    def test_imsave_roundtrip(
        self, shape, dtype, use_pathlib, explicit_photometric_kwarg
    ):
        x = np.random.rand(*shape)

        if not np.issubdtype(dtype, np.floating):
            x = (x * np.iinfo(dtype).max).astype(dtype)
        else:
            x = x.astype(dtype)
        if explicit_photometric_kwarg and x.shape[-1] in [3, 4]:
            kwargs = {'photometric': 'rgb'}
        else:
            kwargs = {}
        self.roundtrip(dtype, x, use_pathlib, **kwargs)
