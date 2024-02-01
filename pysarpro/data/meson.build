python_sources = [
  '__init__.py',
  '__init__.pyi',
  '_binary_blobs.py',
  '_fetchers.py',
  '_registry.py',
]

py3.install_sources(
  python_sources,
  pure: false,             # Will be installed next to binaries
  subdir: 'pysarpro/data'  # Folder relative to site-packages to install to
)

py3.install_sources([
  # See legacy_datasets in _registry.py
  'README.txt',
  'astronaut.png',
  ],
  pure: false,
  subdir: 'pysarpro/data'
)

subdir('tests')
subdir('01-sar')
