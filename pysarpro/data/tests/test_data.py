import os

import pytest

import pysarpro.data as data
from pysarpro._shared.testing import assert_equal
from pysarpro.data._fetchers import _image_fetcher


def test_download_all_with_pooch():
    # jni first wrote this test with the intention of
    # fully deleting the files in the data_dir,
    # then ensure that the data gets downloaded accordingly.
    # hmaarrfk raised the concern that this test wouldn't
    # play well with parallel testing since we
    # may be breaking the global state that certain other
    # tests require, especially in parallel testing

    # The second concern is that this test essentially uses
    # a lot of bandwidth, which is not fun for developers on
    # lower speed connections.
    # https://github.com/Pol-InSAR/pysarpro/pull/4666/files/26d5138b25b958da6e97ebf979e9bc36f32c3568#r422604863
    data_dir = data.data_dir
    if _image_fetcher is not None:
        data.download_all(pattern=r'^data/01-sar')
        assert len(os.listdir(data_dir)) >= 1
    else:
        with pytest.raises(ModuleNotFoundError):
            data.download_all()


def test_astronaut():
    """Test that "astronaut" image can be loaded."""
    astronaut = data.astronaut()
    assert_equal(astronaut.shape, (512, 512, 3))


@pytest.mark.parametrize(
    'function_name',
    [
        'file_hash',
    ],
)
def test_fetchers_are_public(function_name):
    # Check that the following functions that are only used indirectly in the
    # above tests are public.
    assert hasattr(data, function_name)
