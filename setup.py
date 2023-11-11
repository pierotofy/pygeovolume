import setuptools
import sys

with open("README.md", "r") as fh:
    long_description = fh.read()

INSTALL_REQUIRES=[
    'rasterio',
]

setuptools.setup(
    name="pygeovolume",
    version="1.0.0",
    author="Piero Toffanin",
    author_email="pt@uav4geo.com",
    description="Volume calculations on georeferenced raster DEMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pierotofy/pygeovolume",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=INSTALL_REQUIRES
)
