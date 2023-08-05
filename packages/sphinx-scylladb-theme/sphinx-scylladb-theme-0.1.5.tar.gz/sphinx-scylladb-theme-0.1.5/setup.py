# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinx_scylladb_theme', 'sphinx_scylladb_theme.extensions']

package_data = \
{'': ['*'],
 'sphinx_scylladb_theme': ['static/*',
                           'static/css/*',
                           'static/css/doc/*',
                           'static/css/doc/ext/*',
                           'static/fonts/*',
                           'static/img/*',
                           'static/js/*',
                           'static/js/foundation/*',
                           'static/js/vendor/*']}

install_requires = \
['pyyaml>=5.3,<6.0',
 'recommonmark>=0.6.0,<0.7.0',
 'sphinx-copybutton>=0.2.8,<0.3.0',
 'sphinx-tabs>=1.1.13,<2.0.0',
 'sphinx==2.4.4']

setup_kwargs = {
    'name': 'sphinx-scylladb-theme',
    'version': '0.1.5',
    'description': 'A Sphinx Theme for ScyllaDB projects documentation',
    'long_description': None,
    'author': 'David García',
    'author_email': 'dgarcia360@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
