# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pinta', 'pinta.api']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.3.17,<2.0.0',
 'alembic>=1.4.2,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'fastapi>=0.55.1,<0.56.0',
 'kubernetes>=11.0.0,<12.0.0',
 'python-jose[cryptography]>=3.1.0,<4.0.0',
 'rich>=2.0.1,<3.0.0',
 'uvicorn>=0.11.5,<0.12.0']

entry_points = \
{'console_scripts': ['pinta-api = pinta.api.__main__:main']}

setup_kwargs = {
    'name': 'pinta-api',
    'version': '0.0.1',
    'description': 'Job management on GPU clusters',
    'long_description': '# PintaAPI: Job management on GPU clusters 🍺\n\n## Installation\n\nCheck [qed.usc.edu/pinta](https://qed.usc.edu/pinta)\n',
    'author': 'Pinta Team',
    'author_email': 'pinta-l@usc.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://qed.usc.edu/pinta',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
