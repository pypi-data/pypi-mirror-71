# copy from https://raw.githubusercontent.com/kennethreitz/setup.py/master/setup.py

# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
# pip install twine
# pip install wheel
# Usage: setup.py upload

import io
import os
import sys
import datetime
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'pyfunctions'
DESCRIPTION = 'This project contains many functions that can be used in daily development.'
URL = 'https://github.com/broholens/pyfunctions'
EMAIL = 'zzwcng@126.com'
AUTHOR = 'zz'
REQUIRES_PYTHON = '>=3.6.0'

now = datetime.datetime.now()
str_now = str(now).split('.')[0]
VERSION = str_now.replace('-', '.').replace(' ', '.').replace(':', '.')


def load_requirements():
    """load requirements from txt file"""
    with open('requirements.txt', 'r') as req:
        requirements = [line.strip() for line in req.readlines()]
    return requirements

# What packages are required for this module to be executed?
# REQUIRED = [
#     'chardet==3.0.4',
#     'requests==2.21.0',
#     'html2text==2018.1.9',
#     'w3lib==1.20.0',
#     'lxml==4.3.3',
#     'fake-useragent==0.1.11',
#     'selenium==3.141.0'
# ]

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds...')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution...')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine...')
        os.system('twine upload dist/*')

        self.status('Pushing git tags...')
        # remove tag already exists
        # os.system('git tag -d v{0}'.format(about['__version__']))
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    # long_description='https://github.com/broholens/pyfunctions',
    # long_description_content_type='text/text',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],

    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=load_requirements(),
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)