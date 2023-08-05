# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['multiscalemnist']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'h5py>=2.10.0,<3.0.0',
 'numpy>=1.18.4,<2.0.0',
 'opencv-python>=4.2.0,<5.0.0',
 'tqdm>=4.46.0,<5.0.0',
 'yacs>=0.1.7,<0.2.0']

entry_points = \
{'console_scripts': ['multiscalemnist = multiscalemnist.cli:main']}

setup_kwargs = {
    'name': 'multiscalemnist',
    'version': '0.2.1',
    'description': 'MNIST dataset for detection with multiple scales',
    'long_description': None,
    'author': 'PiotrJZielinski',
    'author_email': 'piotrekzie100@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
