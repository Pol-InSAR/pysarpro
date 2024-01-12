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
    "data/astronaut.png": "88431cd9653ccd539741b555fb0a46b61558b301d4110412b5bc28b5e3ea6cb5",
}

registry_urls = {}

legacy_registry = {
    ('data/' + filename): registry['data/' + filename] for filename in legacy_datasets
}
