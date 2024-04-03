"""Standard test images.

For more images, see

 - http://sipi.usc.edu/database/database.php

"""

import os
import os.path as osp
import re
import shutil

from .. import __version__
from ._registry import registry, registry_urls

_LEGACY_DATA_DIR = osp.dirname(__file__)
_DISTRIBUTION_DIR = osp.dirname(_LEGACY_DATA_DIR)

try:
    from pooch import file_hash
except ModuleNotFoundError:
    # Function taken from
    # https://github.com/fatiando/pooch/blob/master/pooch/utils.py
    def file_hash(fname, alg="sha256"):
        """
        Calculate the hash of a given file.
        Useful for checking if a file has changed or been corrupted.
        Parameters
        ----------
        fname : str
            The name of the file.
        alg : str
            The type of the hashing algorithm
        Returns
        -------
        hash : str
            The hash of the file.
        Examples
        --------
        >>> fname = "test-file-for-hash.txt"
        >>> with open(fname, "w") as f:
        ...     __ = f.write("content of the file")
        >>> print(file_hash(fname))
        0fc74468e6a9a829f103d069aeb2bb4f8646bad58bf146bb0e3379b759ec4a00
        >>> import os
        >>> os.remove(fname)
        """
        import hashlib

        if alg not in hashlib.algorithms_available:
            raise ValueError(f'Algorithm \'{alg}\' not available in hashlib')
        # Calculate the hash in chunks to avoid overloading the memory
        chunksize = 65536
        hasher = hashlib.new(alg)
        with open(fname, "rb") as fin:
            buff = fin.read(chunksize)
            while buff:
                hasher.update(buff)
                buff = fin.read(chunksize)
        return hasher.hexdigest()


def _has_hash(path, expected_hash):
    """Check if the provided path has the expected hash."""
    if not osp.exists(path):
        return False
    return file_hash(path) == expected_hash


def _create_image_fetcher():
    try:
        import pooch

        # older versions of Pooch don't have a __version__ attribute
        if not hasattr(pooch, '__version__'):
            retry = {}
        else:
            retry = {'retry_if_failed': 3}
    except ImportError:
        # Without pooch, fallback on the standard data directory
        # which for now, includes a few limited data samples
        return None, _LEGACY_DATA_DIR

    # Pooch expects a `+` to exist in development versions.
    # Since pysarpro doesn't follow that convention, we have to manually
    # remove `.dev` with a `+` if it exists.
    # This helps pooch understand that it should look in master
    # to find the required files
    if '+git' in __version__:
        pysarpro_version_for_pooch = __version__.replace('.dev0+git', '+git')
    else:
        pysarpro_version_for_pooch = __version__.replace('.dev', '+')

    if '+' in pysarpro_version_for_pooch:
        url = "https://github.com/Pol-InSAR/pysarpro/raw/" "{version}/pysarpro/"
    else:
        url = "https://github.com/Pol-InSAR/pysarpro/raw/" "v{version}/pysarpro/"

    # Create a new friend to manage your sample data storage
    image_fetcher = pooch.create(
        # Pooch uses appdirs to select an appropriate directory for the cache
        # on each platform.
        # https://github.com/ActiveState/appdirs
        # On linux this converges to
        # '$HOME/.cache/pysarpro'
        # With a version qualifier
        path=pooch.os_cache("pysarpro"),
        base_url=url,
        version=pysarpro_version_for_pooch,
        version_dev="main",
        env="pysarpro_DATADIR",
        registry=registry,
        urls=registry_urls,
        # Note: this should read `retry_if_failed=3,`, but we generate that
        # dynamically at import time above, in case installed pooch is a less
        # recent version
        **retry,
    )

    data_dir = osp.join(str(image_fetcher.abspath), 'data')
    return image_fetcher, data_dir


_image_fetcher, data_dir = _create_image_fetcher()


def _skip_pytest_case_requiring_pooch(data_filename):
    """If a test case is calling pooch, skip it.

    This running the test suite in environments without internet
    access, skipping only the tests that try to fetch external data.
    """

    # Check if pytest is currently running.
    # Packagers might use pytest to run the tests suite, but may not
    # want to run it online with pooch as a dependency.
    # As such, we will avoid failing the test, and silently skipping it.
    if 'PYTEST_CURRENT_TEST' in os.environ:
        # https://docs.pytest.org/en/latest/example/simple.html#pytest-current-test-environment-variable  #noqa
        import pytest

        # Pytest skip raises an exception that allows the
        # tests to be skipped
        pytest.skip(f'Unable to download {data_filename}', allow_module_level=True)


def _ensure_cache_dir(*, target_dir):
    """Prepare local cache directory if it doesn't exist already.

    Creates::

        /path/to/target_dir/
                 └─ data/
                    └─ README.txt
    """
    os.makedirs(osp.join(target_dir, "data"), exist_ok=True)
    readme_src = osp.join(_DISTRIBUTION_DIR, "data/README.txt")
    readme_dest = osp.join(target_dir, "data/README.txt")
    if not osp.exists(readme_dest):
        shutil.copy2(readme_src, readme_dest)


def _fetch(data_filename):
    """Fetch a given data file from either the local cache or the repository.

    This function provides the path location of the data file given
    its name in the pysarpro repository. If a data file is not included in the
    distribution and pooch is available, it is downloaded and cached.

    Parameters
    ----------
    data_filename : str
        Name of the file in the pysarpro repository. e.g.
        'restoration/tess/camera_rl.npy'.

    Returns
    -------
    file_path : str
        Path of the local file.

    Raises
    ------
    KeyError:
        If the filename is not known to the pysarpro distribution.

    ModuleNotFoundError:
        If the filename is known to the pysarpro distribution but pooch
        is not installed.

    ConnectionError:
        If pysarpro is unable to connect to the internet but the
        dataset has not been downloaded yet.
    """
    expected_hash = registry[data_filename]
    if _image_fetcher is None:
        cache_dir = osp.dirname(data_dir)
    else:
        cache_dir = str(_image_fetcher.abspath)

    # Case 1: the file is already cached in `data_cache_dir`
    cached_file_path = osp.join(cache_dir, data_filename)
    if _has_hash(cached_file_path, expected_hash):
        # Nothing to be done, file is where it is expected to be
        return cached_file_path

    # Case 2: file is present in `legacy_data_dir`
    legacy_file_path = osp.join(_DISTRIBUTION_DIR, data_filename)
    if _has_hash(legacy_file_path, expected_hash):
        return legacy_file_path

    # Case 3: file is not present locally
    if _image_fetcher is None:
        _skip_pytest_case_requiring_pooch(data_filename)
        raise ModuleNotFoundError(
            "The requested file is part of the pysarpro distribution, "
            "but requires the installation of an optional dependency, pooch. "
            "To install pooch, use your preferred python package manager. "
            "Follow installation instruction found at "
            "https://pol-insar.github.io/docs/stable/user_guide/install.html"
        )
    # Download the data with pooch which caches it automatically
    _ensure_cache_dir(target_dir=cache_dir)
    try:
        cached_file_path = _image_fetcher.fetch(data_filename)
        return cached_file_path
    except ConnectionError as err:
        _skip_pytest_case_requiring_pooch(data_filename)
        # If we decide in the future to suppress the underlying 'requests'
        # error, change this to `raise ... from None`. See PEP 3134.
        raise ConnectionError(
            'Tried to download a pysarpro dataset, but no internet '
            'connection is available. To avoid this message in the '
            'future, try `pysarpro.data.download_all()` when you are '
            'connected to the internet.'
        ) from err


def download_all(directory=None, pattern=None):
    """Download all datasets for use with pysarpro offline.

    pysarpro datasets are no longer shipped with the library by default.
    This allows us to use higher quality datasets, while keeping the
    library download size small.

    This function requires the installation of an optional dependency, pooch,
    to download the full dataset. Follow installation instruction found at

        https://pol-insar.github.io/docs/stable/user_guide/install.html

    Call this function to download all sample images making them available
    offline on your machine.

    Parameters
    ----------
    directory: path-like, optional
        The directory where the dataset should be stored.
    pattern: str, optional
        A regex pattern to filter the datasets to be downloaded.

    Raises
    ------
    ModuleNotFoundError:
        If pooch is not install, this error will be raised.

    Notes
    -----
    pysarpro will only search for images stored in the default directory.
    Only specify the directory if you wish to download the images to your own
    folder for a particular reason. You can access the location of the default
    data directory by inspecting the variable ``pysarpro.data.data_dir``.
    """

    if _image_fetcher is None:
        raise ModuleNotFoundError(
            "To download all package data, pysarpro needs an optional "
            "dependency, pooch."
            "To install pooch, follow our installation instructions found at "
            "https://pol-insar.github.io/docs/stable/user_guide/install.html"
        )
    # Consider moving this kind of logic to Pooch
    old_dir = _image_fetcher.path
    try:
        if directory is not None:
            directory = osp.expanduser(directory)
            _image_fetcher.path = directory
        _ensure_cache_dir(target_dir=_image_fetcher.path)

        for data_filename in _image_fetcher.registry:
            if pattern is not None and not re.search(pattern, data_filename):
                continue
            file_path = _fetch(data_filename)

            # Copy to `directory` or implicit cache if it is not already there
            if not file_path.startswith(str(_image_fetcher.path)):
                dest_path = osp.join(_image_fetcher.path, data_filename)
                os.makedirs(osp.dirname(dest_path), exist_ok=True)
                shutil.copy2(file_path, dest_path)
    finally:
        _image_fetcher.path = old_dir


def lbp_frontal_face_cascade_filename():
    """Return the path to the XML file containing the weak classifier cascade.

    These classifiers were trained using LBP features. The file is part
    of the OpenCV repository [1]_.

    References
    ----------
    .. [1] OpenCV lbpcascade trained files
           https://github.com/opencv/opencv/tree/master/data/lbpcascades
    """

    return _fetch('data/lbpcascade_frontalface_opencv.xml')


def _load(f, as_gray=False):
    """Load an image file located in the data directory.

    Parameters
    ----------
    f : string
        File name.
    as_gray : bool, optional
        Whether to convert the image to grayscale.

    Returns
    -------
    img : ndarray
        Image loaded from ``pysarpro.data_dir``.
    """
    # importing io is quite slow since it scans all the backends
    # we lazy import it here
    from ..io import imread

    return imread(_fetch(f), as_gray=as_gray)


def astronaut():
    """Color image of the astronaut Eileen Collins.

    Photograph of Eileen Collins, an American astronaut. She was selected
    as an astronaut in 1992 and first piloted the space shuttle STS-63 in
    1995. She retired in 2006 after spending a total of 38 days, 8 hours
    and 10 minutes in outer space.

    This image was downloaded from the NASA Great Images database
    <https://flic.kr/p/r9qvLn>`__.

    No known copyright restrictions, released into the public domain.

    Returns
    -------
    astronaut : (512, 512, 3) uint8 ndarray
        Astronaut image.
    """

    return _load("data/astronaut.png")
