import numpy as np
import pytest

from pysarpro.io import imread, imsave, plugin_order, reset_plugins, use_plugin

pytest.importorskip('SimpleITK')


@pytest.fixture(autouse=True)
def use_simpleitk_plugin():
    """Ensure that SimpleITK plugin is used."""
    use_plugin('simpleitk')
    yield
    reset_plugins()


def test_prefered_plugin():
    order = plugin_order()
    assert order["imread"][0] == "simpleitk"
    assert order["imsave"][0] == "simpleitk"
    assert order["imread_collection"][0] == "simpleitk"


@pytest.mark.parametrize("shape", [(10, 10), (10, 10, 3), (10, 10, 4)])
@pytest.mark.parametrize("dtype", [np.uint8, np.uint16, np.float32, np.float64])
def test_imsave_roundtrip(shape, dtype, tmp_path):
    if np.issubdtype(dtype, np.floating):
        info_func = np.finfo
    else:
        info_func = np.iinfo
    expected = np.linspace(
        info_func(dtype).min,
        info_func(dtype).max,
        endpoint=True,
        num=np.prod(shape),
        dtype=dtype,
    )
    expected = expected.reshape(shape)
    file_path = tmp_path / "roundtrip.mha"
    imsave(file_path, expected)
    actual = imread(file_path)
    np.testing.assert_array_almost_equal(actual, expected)
