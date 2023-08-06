from os import path

from setuptools import setup, find_packages

# To use a consistent encoding
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.rst')) as f:
    LONG_DESCRIPTION = f.read()

# Get the version number from the version.txt
with open(path.join(HERE, 'version.txt')) as f:
    VERSION = f.read()

with open(path.join(HERE, 'wavelength_test/requirements.txt')) as f:
    requires = f.read().splitlines()

setup(name='wavelength-test',
      version=VERSION,
      description='Common Utilities for Serverless Testing',
      long_description=LONG_DESCRIPTION,
      classifiers=[
          'Programming Language :: Python :: 3'
      ],
      keywords='Lambda, Serverless, AWS, Integration Testing, Testing, Local Development',
      author='Wavelength Serverless Team',
      author_email="dev@teamwavelength.com",
      packages=find_packages(exclude=['test*']),
      include_package_data=True,
      package_dir={'.': ''},
      install_requires=requires,
      zip_safe=False)
