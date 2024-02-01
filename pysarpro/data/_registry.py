# flake8: noqa

# This minimal dataset was available as part of
# pysarpro 0.15 and will be retained until
# further notice.
# Testing data and additional datasets should only
# be made available by pooch
legacy_datasets = [
    'astronaut.png',
    '01-sar/signal1_ac.npy',
    '01-sar/signal1_rc.npy',
    '01-sar/signal2_ac.npy',
    '01-sar/signal2_rc.npy',
]

# Registry of datafiles that can be downloaded along with their SHA256 hashes
# To generate the SHA256 hash, use the command
# openssl sha256 filename
registry = {
    "data/astronaut.png": "88431cd9653ccd539741b555fb0a46b61558b301d4110412b5bc28b5e3ea6cb5",
    "data/01-sar/signal1_ac.npy": "814e847e979c6ae0c9cda290c7f6b2d7ed2bf212cf8b454a8671abf1f9d5df52",
    "data/01-sar/signal1_rc.npy": "30f43d643b162eda34061b72bf64bc9a4e1893cfdb309e1e577fa9ba19e629af",
    "data/01-sar/signal2_ac.npy": "ed62d3d0e8a7c52f6b031493f537304c77b7fd833dd8820578cb847bbcc42d60",
    "data/01-sar/signal2_rc.npy": "8c3b01775eebfcb1795aaaab9396928c3251c21d9cfe3b0484ce0e9624640138",
}

registry_urls = {}

legacy_registry = {
    ('data/' + filename): registry['data/' + filename] for filename in legacy_datasets
}
