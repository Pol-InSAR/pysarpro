# from tempfile import NamedTemporaryFile

# import numpy as np
# import pytest

# from pysarpro.io import imread, imsave

# def test_prefered_plugin():
#     # Don't call use_plugin("imageio") before, this way we test that imageio is used
#     # by default
#     order = plugin_order()
#     assert order["imread"][0] == "imageio"
#     assert order["imsave"][0] == "imageio"
#     assert order["imread_collection"][0] == "imageio"


# class TestSave:
#     @pytest.mark.parametrize(
#         "shape,dtype",
#         [
#             # float32, float64 can't be saved as PNG and raise
#             # uint32 is not roundtripping properly
#             ((10, 10), np.uint8),
#             ((10, 10), np.uint16),
#             ((10, 10, 2), np.uint8),
#             ((10, 10, 3), np.uint8),
#             ((10, 10, 4), np.uint8),
#         ],
#     )
#     def test_imsave_roundtrip(self, shape, dtype, tmp_path):
#         if np.issubdtype(dtype, np.floating):
#             min_ = 0
#             max_ = 1
#         else:
#             min_ = 0
#             max_ = np.iinfo(dtype).max
#         expected = np.linspace(
#             min_, max_, endpoint=True, num=np.prod(shape), dtype=dtype
#         )
#         expected = expected.reshape(shape)
#         file_path = tmp_path / "roundtrip.png"
#         imsave(file_path, expected)
#         actual = imread(file_path)
#         np.testing.assert_array_almost_equal(actual, expected)

#     def test_bool_array_save(self):
#         with NamedTemporaryFile(suffix='.png') as f:
#             fname = f.name

#         with pytest.warns(UserWarning, match=r'.* is a boolean image'):
#             a = np.zeros((5, 5), bool)
#             a[2, 2] = True
#             imsave(fname, a)
