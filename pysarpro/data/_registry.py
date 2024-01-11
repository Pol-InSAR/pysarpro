# flake8: noqa

# This minimal dataset was available as part of
# pysarpro 0.15 and will be retained until
# further notice.
# Testing data and additional datasets should only
# be made available by pooch
legacy_datasets = [
    'astronaut.png',
]

# Registry of datafiles that can be downloaded along with their SHA256 hashes
# To generate the SHA256 hash, use the command
# openssl sha256 filename
registry = {
    "color/tests/data/lab_array_a_10.npy": "a3ef76f1530e374f9121020f1f220bc89767dc866f4bbd1b1f47e5b84891a38c",
}

registry_urls = {
    "data/cells3d.tif": "https://gitlab.com/Pol-InSAR/data/-/raw/2cdc5ce89b334d28f06a58c9f0ca21aa6992a5ba/cells3d.tif"
}

legacy_registry = {
    ('data/' + filename): registry['data/' + filename] for filename in legacy_datasets
}
