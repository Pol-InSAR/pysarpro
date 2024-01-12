#!/bin/bash
# Script to download / check and upload pysarpro wheels for release
if [ "`which twine`" == "" ]; then
    echo "twine not on path; need to pip install twine?"
    exit 1
fi
if [ "`which wheel-uploader`" == "" ]; then
    echo "wheel-uploader not on path; see https://github.com/MacPython/terryfy"
    exit 1
fi
PYSAR_VERSION=`git describe --tags`
if [ "${PYSAR_VERSION:0:1}" != 'v' ]; then
    echo "pysarpro version $PYSAR_VERSION does not start with 'v'"
    exit 1
fi
echo "Trying download / upload of version ${PYSAR_VERSION:1}"
wheel-uploader -v pysarpro "${PYSAR_VERSION:1}"
wheel-uploader -v pysarpro -t manylinux1 "${PYSAR_VERSION:1}"
wheel-uploader -v pysarpro -t win "${PYSAR_VERSION:1}"
