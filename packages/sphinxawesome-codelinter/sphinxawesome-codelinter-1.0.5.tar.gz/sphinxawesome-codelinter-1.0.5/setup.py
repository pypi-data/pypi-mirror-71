# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sphinxawesome', 'sphinxawesome.codelinter']

package_data = \
{'': ['*']}

install_requires = \
['sphinx>=2.2,<4.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6.1,<2.0.0']}

setup_kwargs = {
    'name': 'sphinxawesome-codelinter',
    'version': '1.0.5',
    'description': 'A Sphinx extension to pass reStructuredText code blocks to external tools.',
    'long_description': '# Sphinx awesome codelinter\n\n[![License](https://img.shields.io/github/license/kai687/sphinxawesome-codelinter?color=blue&style=for-the-badge)](https://github.com/kai687/sphinxawesome-codelinter/blob/master/LICENSE)\n[![PyPI version](https://img.shields.io/pypi/v/sphinxawesome-codelinter?style=for-the-badge)](https://pypi.org/project/sphinxawesome-codelinter)\n[![PyTest Status](https://img.shields.io/github/workflow/status/kai687/sphinxawesome-codelinter/Run%20unit%20tests%20against%20different%20versions%20of%20Python?label=tests&style=for-the-badge)](https://github.com/kai687/sphinxawesome-codelinter/actions?query=workflow%3A%22Run+unit+tests%22)\n[![Codecov](https://img.shields.io/codecov/c/gh/kai687/sphinxawesome-codelinter?style=for-the-badge)](https://codecov.io/gh/kai687/sphinxawesome-codelinter)\n![Supported Python Versions](https://img.shields.io/pypi/pyversions/sphinxawesome-codelinter?style=for-the-badge)\n![Code style](https://img.shields.io/badge/Code%20Style-Black-000000?style=for-the-badge)\n\nThis extension for the Sphinx documentation generator allows you to expose code blocks\nin your documentation to an external tool. This can be used to check that code blocks\ncontain only valid code. For more information about the Sphinx project, visit the\nwebsite at http://www.sphinx-doc.org/.\n\nThis extension provides a new builder: `sphinx-build -b codelinter`.\n\n## Installation\n\nInstall the extension:\n\n```console\npip install sphinxawesome-codelinter\n```\n\nThis Sphinx extension should work with Python versions newer than 3.6 and recent Sphinx\nreleases.\n\n## Configuration\n\nTo enable this extension in Sphinx, add it to the list of extensions in the Sphinx\nconfiguration file `conf.py`:\n\n```python\nextensions = ["sphinxawesome.codelinter"]\n```\n\nTo pass code blocks to an external tool, provide the language as a key and the tool as\nthe associated value to the `codelinter_languages` dictionary. This dictionary is\ninitially empty, so even if the extension is installed and included in the `extensions`\nlist, no code blocks will be processed by default.\n\nFor example, to pass all JSON blocks to the python builtin JSON module, use:\n\n```python\ncodelinter_languages = {\n  "json": "python -m json.tool"\n}\n```\n\nThe python command returns an error for non-valid JSON code. For linting YAML code\nblocks, you could install the `yamllint` tool and then add:\n\n```python\ncodelinter_languages = {\n  "yaml": "yamllint -"\n}\n```\n\nThe `-` tells yamllint to read from `stdin`. You can also write your own tools that can\nread from `stdin` and write to `stdout` or `stderr`. The only expectation is that any\ntools returns a value of 0 if no errors were found, a non-zero value otherwise.\n\nYou can use any reStructuredText directive that gets parsed as a `literal_block` node.\nFor example, you can use `.. code-block:: json` as well as `.. highlight:: json`.\n\nYou can also use the `..literalinclude:: <filename>` directive to include code from\nfiles.\n\n```\n.. literalinclude:: code.json\n   :language: json\n```\n\n> **Caution:** The value of the `codelinter_languages` dictionary will be called as\n> provided. No additional safe-guards are in place to prevent abuse.\n\n## Use\n\nUse `sphinx-build -b codelinter` like you would use other Sphinx builders. No output\nwill be written to disk. If the codelinter tool exits with a non-zero return value, a\nwarning will be logged. You can use the `sphinx-build -W` option to turn those warnings\ninto errors to stop the build process.\n',
    'author': 'Kai Welke',
    'author_email': 'kai687@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kai687/sphinxawesome-codelinter',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
