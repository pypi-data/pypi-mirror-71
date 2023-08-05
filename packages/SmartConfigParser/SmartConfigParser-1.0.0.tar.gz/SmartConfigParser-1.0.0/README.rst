SmartConfigParser
==================

.. image:: https://travis-ci.org/ricard33/smartconfigparser.png
   :target: https://travis-ci.org/ricard33/smartconfigparser

Builds on top of the builtin SafeConfigParser but adds various
convenience functionalities like default values.

.. code:: python

    from smartconfigparser import Config

    config = Config()
    config.read('config.ini')

    user = config.get('SECTION', 'user', 'John')
    age = config.getint('SECTION', 'age', 28)
    weight = config.getfloat('SECTION', 'weight', 80.2)
    is_developer = config.getboolean('SECTION', 'is_developer', True)
    hobbies = config.getlist('SECTION', 'hobbies', ['diving', 'making software'])

    # if SECTION does not exist in config.ini get default values
    print(user, age, weight, is_developer, hobbies)
    # ('John', 28, 80.2, True, ['diving', 'making software'])

Installation
============

Install it with pip:

    pip install smartconfigparser


Test
====

run tests

    python test_smartconfigparser.py

Example
=======

DJANGO default settings file

.. code:: python

    import os
    from smartconfigparser import Config

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    CONFIG_PATH = os.path.join(BASE_DIR, 'config')
    if not os.path.exists(CONFIG_PATH):
        os.makedirs(CONFIG_PATH)

    CONFIG_FILE = os.path.join(CONFIG_PATH, 'config.ini')
    config = Config()
    config.read(CONFIG_FILE)

    try:
        SECRET_KEY = config.get('DJANGO', 'SECRET_KEY')
    except:
        print('SECRET_KEY not found! Generating a new one...')
        import random

        SECRET_KEY = "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$^&*(-_=+)") for i in range(50)])
        if not config.has_section('DJANGO'):
            config.add_section('DJANGO')
        config.set('DJANGO', 'SECRET_KEY', SECRET_KEY)
        with open(CONFIG_FILE, 'wt') as f:
            config.write(f)

    DEBUG = config.getboolean('DJANGO', 'DEBUG', False)

    ALLOWED_HOSTS = config.getlist('DJANGO', 'ALLOWED_HOSTS', ['localhost', '127.0.0.1'])

    # ...

    DATABASES = {
        'default': {
            'ENGINE': config.get('DATABASE', 'engine', 'django.db.backends.sqlite3'),
            'NAME': config.get('DATABASE', 'name', 'db.sqlite3'),
            'USER': config.get('DATABASE', 'user', ''),
            'PASSWORD': config.get('DATABASE', 'password', ''),
            'HOST': config.get('DATABASE', 'host', ''),
            'PORT': config.get('DATABASE', 'port', ''),
        }
    }


config.ini file for a developer
::

    [DJANGO]
    DEBUG = True


config.ini file for production server
::

    [DATABASE]
    engine = django.db.backends.postgresql
    name = database
    user = postgres_db_user
    password = very_strong_password
    host = localhost
    port = 5432


Usage
=====

smartconfigparser.get
---------------------

config.get(section, option, default_value)

same as ConfigParser.get() method except that it return default value if section or option does not exists
    
    
smartconfigparser.getint
------------------------

config.getint(section, option, default_value)

same as ConfigParser.getint() method except that it return default value if section or option does not exists


smartconfigparser.getfloat
--------------------------

config.getfloat(section, option, default_value)

same as ConfigParser.getfloat() method except that it return default value if section or option does not exists


smartconfigparser.getboolean
----------------------------

config.getboolean(section, option, default_value)

same as ConfigParser.getboolean() method except that it return default value if section or option does not exists


smartconfigparser.getlist
-------------------------

config.getlist(section, option, default_list)

Return a list of the words in the option value, using comma (',') as the delimiter string

config.ini file 
::

    [section]
    list = a,b,c

example 

.. code:: python

    print(config.getlist('section', 'list', []))
    # ['a', 'b', 'c']
    print(config.getlist('section_does_not_exists', 'list', []))
    # []

smartconfigparser.set
---------------------

config.set(section, option, value)

same as ConfigParser.set() method except that it create section if section does not exists

example 

.. code:: python

    from smartconfigparser import Config

    config = Config()
    config.set('section_does_not_exist', 'user', 'John DOE')
    with open('config.ini', 'wt') as configfile:
        config.write(configfile)

config.ini
::

    [section_does_not_exist]
    user = John DOE


License
=======
MIT - See LICENSE file
