# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pre_commit_run_hook_entry']
install_requires = \
['pre-commit>=2.4.0,<3.0.0']

entry_points = \
{'console_scripts': ['pre-commit-run-black-entry = '
                     'pre_commit_run_hook_entry:main_black',
                     'pre-commit-run-hook-entry = '
                     'pre_commit_run_hook_entry:main']}

setup_kwargs = {
    'name': 'pre-commit-run-hook-entry',
    'version': '1.0.0a1',
    'description': 'Run pre-commit hook entry. Allow to run pre-commit hooks for text editor formatting / linting needs.',
    'long_description': '=========================\npre-commit-run-hook-entry\n=========================\n\n.. image:: https://github.com/playpauseandstop/pre-commit-run-hook-entry/workflows/ci/badge.svg\n    :target: https://github.com/playpauseandstop/pre-commit-run-hook-entry/actions?query=workflow%3A%22ci%22\n    :alt: CI Workflow\n\n.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n    :target: https://github.com/pre-commit/pre-commit\n    :alt: pre-commit\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: black\n\n.. image:: https://img.shields.io/pypi/v/pre-commit-run-hook-entry.svg\n    :target: https://pypi.org/project/pre-commit-run-hook-entry/\n    :alt: Latest Version\n\n.. image:: https://img.shields.io/pypi/pyversions/pre-commit-run-hook-entry.svg\n    :target: https://pypi.org/project/pre-commit-run-hook-entry/\n    :alt: Python versions\n\n.. image:: https://img.shields.io/pypi/l/pre-commit-run-hook-entry.svg\n    :target: https://github.com/playpauseandstop/pre-commit-run-hook-entry/blob/master/LICENSE\n    :alt: BSD License\n\n.. image:: https://coveralls.io/repos/playpauseandstop/pre-commit-run-hook-entry/badge.svg?branch=master&service=github\n    :target: https://coveralls.io/github/playpauseandstop/pre-commit-run-hook-entry\n    :alt: Coverage\n\nRun `pre-commit`_ hook entry. Allow to run pre-commit hooks for text editor\nformatting / linting needs.\n\n.. _`pre-commit`: https://pre-commit.com/\n\nRequirements\n============\n\n- `Python <https://www.python.org/>`_ 3.7 or later\n- `pre-commit`_ 2.4.0 or later\n\nLicense\n=======\n\n``pre-commit-run-hook-entry`` is licensed under the terms of\n`BSD-3-Clause </LICENSE>`_ license.\n\nInstallation\n============\n\n.. code-block:: bash\n\n    pip install pre-commit-run-hook-entry\n\nUsage\n=====\n\n.. code-block:: bash\n\n    pre-commit-run-hook-entry HOOK\n\nPrerequisites\n-------------\n\n``pre-commit-run-hook-entry`` only works in directories, where\n``pre-commit run --all HOOK`` is executable.\n\nVS Code Integration\n-------------------\n\nExample below illustrates how to configure VS Code to use black, flake8 &\nmypy pre-commit hooks for formatting & linting,\n\n.. code-block:: json\n\n    {\n        "python.formatting.provider": "black",\n        "python.formatting.blackPath": "pre-commit-run-hook-entry",\n        "python.formatting.blackArgs": ["black"],\n        "python.linting.enabled": true,\n        "python.linting.flake8Enabled": true,\n        "python.linting.flake8Path": "pre-commit-run-hook-entry",\n        "python.linting.flake8Args": ["flake8"],\n        "python.linting.mypyEnabled": true,\n        "python.linting.mypyPath": "pre-commit-run-hook-entry",\n        "python.linting.mypyArgs": ["mypy"]\n    }\n\nSublime Text 3 Integration\n--------------------------\n\nsublack\n~~~~~~~\n\nFrom one point `sublack <https://github.com/jgirardet/sublack/>`__ has builtin\npre-commit integration, but it seems do not respect settings from\n``pyproject.toml``, to fix this use ``pre-commit-run-black-entry`` as\n``sublack.black_command``,\n\n.. code-block:: json\n\n    {\n        "sublack.black_command": "pre-commit-run-black-entry"\n    }\n\n\nSublimeLinter-contrib-flake8\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n.. code-block:: json\n\n    {\n        "SublimeLinter.linters.flake8.executable": "pre-commit-run-hook-entry",\n        "SublimeLinter.linters.flake8.args": ["--", "flake8"]\n    }\n\n\nSublimeLinter-contrib-mypy\n~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n.. code-block:: json\n\n    {\n        "SublimeLinter.linters.mypy.executable": "pre-commit-run-hook-entry",\n        "SublimeLinter.linters.mypy.args": ["--", "mypy"]\n    }\n\nIssues & Feature Requests\n=========================\n\nFeel free to submit new issue or feature request `at GitHub\n<https://github.com/playpauseandstop/pre-commit-run-hook-entry/issues>`_\n',
    'author': 'Igor Davydenko',
    'author_email': 'iam@igordavydenko.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://igordavydenko.com/projects/#pre-commit-run-hook-entry',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
