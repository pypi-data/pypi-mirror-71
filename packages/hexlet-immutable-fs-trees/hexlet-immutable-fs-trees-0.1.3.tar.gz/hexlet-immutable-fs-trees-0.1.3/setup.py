# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['__init__']
setup_kwargs = {
    'name': 'hexlet-immutable-fs-trees',
    'version': '0.1.3',
    'description': '',
    'long_description': '# python-immutable-fs-trees\n\n[![Hexlet Ltd. logo](https://raw.githubusercontent.com/Hexlet/hexletguides.github.io/master/images/hexlet_logo128.png)](https://ru.hexlet.io/pages/about)\n\nThis repository is created and maintained by the team and the community of Hexlet, an educational project. [Read more about Hexlet (in Russian)](https://ru.hexlet.io/pages/about?utm_source=github&utm_medium=link&utm_campaign=python-immutable-fs-trees).\n',
    'author': 'Hexlet Team',
    'author_email': 'info@hexlet.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hexlet-components/python-immutable-fs-trees',
    'package_dir': package_dir,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
