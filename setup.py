# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import version

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
   
    name='seasonality_removal',  
    version=version.__version__,
    description='A python project that removes the seasonality from timeseries when a date column is available',
    url='https://github.com/admdemiraj/SeasonalityRemoval',
    python_requires='>=3',
    author='Admir Demiraj',
    license='MIT',
    author_email='admdemiraj@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    keywords='seasonality_removal timeseries seasonal_adjustment seasonal_indexes',
    scripts = ["runner"],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
   
)

