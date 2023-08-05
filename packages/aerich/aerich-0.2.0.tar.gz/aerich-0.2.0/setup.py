# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aerich',
 'aerich.ddl',
 'aerich.ddl.mysql',
 'aerich.ddl.postgres',
 'aerich.ddl.sqlite']

package_data = \
{'': ['*']}

install_requires = \
['asyncclick', 'pydantic', 'tortoise-orm']

extras_require = \
{'dbdrivers': ['aiomysql', 'asyncpg']}

entry_points = \
{'console_scripts': ['aerich = aerich.cli:main']}

setup_kwargs = {
    'name': 'aerich',
    'version': '0.2.0',
    'description': 'A database migrations tool for Tortoise ORM.',
    'long_description': '======\nAerich\n======\n\n.. image:: https://img.shields.io/pypi/v/aerich.svg?style=flat\n   :target: https://pypi.python.org/pypi/aerich\n.. image:: https://img.shields.io/github/license/long2ice/aerich\n   :target: https://github.com/long2ice/aerich\n.. image:: https://github.com/long2ice/aerich/workflows/pypi/badge.svg\n   :target: https://github.com/long2ice/aerich/actions?query=workflow:pypi\n.. image:: https://github.com/long2ice/aerich/workflows/test/badge.svg\n   :target: https://github.com/long2ice/aerich/actions?query=workflow:test\n\nIntroduction\n============\n\nTortoise-ORM is the best asyncio ORM now, but it lacks a database migrations tool like alembic for SQLAlchemy, or Django ORM with it\'s own migrations tool.\n\nThis project aim to be a best migrations tool for Tortoise-ORM and which written by one of contributors of Tortoise-ORM.\n\nInstall\n=======\n\nJust install from pypi:\n\n.. code-block:: shell\n\n    $ pip install aerich\n\nQuick Start\n===========\n\n.. code-block:: shell\n\n    $ aerich -h\n\n    Usage: aerich [OPTIONS] COMMAND [ARGS]...\n\n    Options:\n      -c, --config TEXT  Config file.  [default: aerich.ini]\n      --app TEXT         Tortoise-ORM app name.  [default: models]\n      -n, --name TEXT    Name of section in .ini file to use for aerich config.\n                         [default: aerich]\n      -h, --help         Show this message and exit.\n\n    Commands:\n      downgrade  Downgrade to previous version.\n      heads      Show current available heads in migrate location.\n      history    List all migrate items.\n      init       Init config file and generate root migrate location.\n      init-db    Generate schema and generate app migrate location.\n      migrate    Generate migrate changes file.\n      upgrade    Upgrade to latest version.\n\nUsage\n=====\nYou need add ``aerich.models`` to your ``Tortoise-ORM`` config first, example:\n\n.. code-block:: python\n\n    TORTOISE_ORM = {\n        "connections": {"default": "mysql://root:123456@127.0.0.1:3306/test"},\n        "apps": {\n            "models": {\n                "models": ["tests.models", "aerich.models"],\n                "default_connection": "default",\n            },\n        },\n    }\n\nInitialization\n--------------\n\n.. code-block:: shell\n\n    $ aerich init -h\n\n    Usage: aerich init [OPTIONS]\n\n      Init config file and generate root migrate location.\n\n    Options:\n      -t, --tortoise-orm TEXT  Tortoise-ORM config module dict variable, like settings.TORTOISE_ORM.\n                               [required]\n      --location TEXT          Migrate store location.  [default: ./migrations]\n      -h, --help               Show this message and exit.\n\nInit config file and location:\n\n.. code-block:: shell\n\n    $ aerich init -t tests.backends.mysql.TORTOISE_ORM\n\n    Success create migrate location ./migrations\n    Success generate config file aerich.ini\n\nInit db\n-------\n\n.. code-block:: shell\n\n    $ aerich init-db\n\n    Success create app migrate location ./migrations/models\n    Success generate schema for app "models"\n\n.. note::\n\n    If your Tortoise-ORM app is not default ``models``, you must specify ``--app`` like ``aerich --app other_models init-db``.\n\nUpdate models and make migrate\n------------------------------\n\n.. code-block:: shell\n\n    $ aerich migrate --name drop_column\n\n    Success migrate 1_202029051520102929_drop_column.json\n\nFormat of migrate filename is ``{version_num}_{datetime}_{name|update}.json``\n\nUpgrade to latest version\n-------------------------\n\n.. code-block:: shell\n\n    $ aerich upgrade\n\n    Success upgrade 1_202029051520102929_drop_column.json\n\nNow your db is migrated to latest.\n\nDowngrade to previous version\n-----------------------------\n\n.. code-block:: shell\n\n    $ aerich downgrade\n\n    Success downgrade 1_202029051520102929_drop_column.json\n\nNow your db rollback to previous version.\n\nShow history\n------------\n\n.. code-block:: shell\n\n    $ aerich history\n\n    1_202029051520102929_drop_column.json\n\nShow heads to be migrated\n-------------------------\n\n.. code-block:: shell\n\n    $ aerich heads\n\n    1_202029051520102929_drop_column.json\n\nLimitations\n===========\n* Not support ``rename column`` now.\n* ``Sqlite`` and ``Postgres`` may not work as expected because I don\'t use those in my work.\n\nLicense\n=======\nThis project is licensed under the `MIT <https://github.com/long2ice/aerich/blob/master/LICENSE>`_ License.\n',
    'author': 'long2ice',
    'author_email': 'long2ice@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/long2ice/aerich',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
