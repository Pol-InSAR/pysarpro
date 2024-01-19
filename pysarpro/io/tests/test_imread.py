from tempfile import NamedTemporaryFile

import numpy as np
from pytest import importorskip

from pysarpro import io
from pysarpro._shared import testing
from pysarpro._shared.testing import (
    TestCase,
    assert_array_almost_equal,
    assert_array_equal,
    fetch,
)
from pysarpro.io import imread, imsave, reset_plugins, use_plugin

importorskip('imread')


def setup():
    use_plugin('imread')


def teardown():
    reset_plugins()


def test_imread_as_gray():
    img = imread(fetch('data/color.png'), as_gray=True)
    assert img.ndim == 2
    assert img.dtype == np.float64
    img = imread(fetch('data/astronaut.png'), as_gray=True)
    # check that conversion does not happen for a gray image
    assert np.core.numerictypes.sctype2char(img.dtype) in np.typecodes['AllInteger']


def test_imread_palette():
    img = imread(fetch('data/palette_color.png'))
    assert img.ndim == 3


def test_imread_truncated_jpg():
    with testing.raises(RuntimeError):
        io.imread(fetch('data/truncated.jpg'))


def test_bilevel():
    expected = np.zeros((10, 10), bool)
    expected[::2] = 1

    img = imread(fetch('data/checker_bilevel.png'))
    assert_array_equal(img.astype(bool), expected)


class TestSave(TestCase):
    def roundtrip(self, x, scaling=1):
        with NamedTemporaryFile(suffix='.png') as f:
            fname = f.name

        imsave(fname, x)
        y = imread(fname)

        assert_array_almost_equal((x * scaling).astype(np.int32), y)

    def test_imsave_roundtrip(self):
        dtype = np.uint8
        np.random.seed(0)
        for shape in [(10, 10), (10, 10, 3), (10, 10, 4)]:
            x = np.ones(shape, dtype=dtype) * np.random.rand(*shape)

            if np.issubdtype(dtype, np.floating):
                yield self.roundtrip, x, 255
            else:
                x = (x * 255).astype(dtype)
                yield self.roundtrip, x
