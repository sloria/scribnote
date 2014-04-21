==============
Psygist Server
==============

Code gists for neurophysiological tasks


Quickstart
----------

::

    pip install -r requirements/dev.txt
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    python manage.py server



Deployment
----------

In your production environment, make sure the ``PSYGIST_ENV`` environment variable is set to ``"prod"``.


Running Tests
-------------

To run all tests, run ::

    invoke test


Migrations
----------

Whenever a database migration needs to be made. Run the following commmands:
::

    python manage.py db migrate

This will generate a new migration script. Then run:
::

    python manage.py db upgrade

To apply the migration.

For a full migration command reference, run ``python manage.py db --help``.
