nuvolos - The database connectivity library for Nuvolos
=======================================================

Installation
============

.. code:: bash

    $ pip install nuvolos 

Usage
=====
The library provides two convenience functions for connecting to the remote database with your credentials. There are two possible usage modes. 

1. If you are running python in a Nuvolos application (e.g. JupyterLab), you don't have to provide any arguments or credentials for the library to create a SQLALchemy engine.
2. If you are running python from a non-Nuvolos application (e.g. your own computer), you have to provide four arguments: your username, your database password, the database and schema of the dataset you want to connect to. This information can be found in the Connection guide in the Nuvolos UI. 

Using in Nuvolos applications
=============================

You can get the SQLAlchemy connection string or create an SQLAlchemy engine directly, or even obtain a SQLAlchemy connection object from an engine:

::

    >>> from nuvolos import get_url, get_engine, get_connection
    >>> get_url()
    'snowflake://<username>:<password>@alphacruncher.eu-central-1/?database=%22<dbname>%22&schema=%22<schemaname>%22'
    >>> get_url(username="abc", password="def", dbname="db_name", schemaname="schema_name")
    'snowflake://abc:def@alphacruncher.eu-central-1/&database=db_name&schema=schema_name'
    >>> eng = get_engine()
    >>> con = get_connection()

In general, we suggest using :code:`get_connection()` to obtain a SQLAlchemy connection that you can execute statements with.

Using in non-Nuvolos applications
==================================

You can get the SQLALchemy connection string, SQLAlchemy engine or SQLAlchemy connection as with Nuvolos, however you will have to provide all four arguments:

::

   >>> from nuvolos import get_url, get_engine, get_connection
   >>> get_url(username="username", password = "password", dbname = "dbname", schemaname="schemaname")
   'snowflake://username:password@alphacruncher.eu-central-1/?database=%22dbname%22&schema=%22schemaname%22'
   >>> eng = get_engine(username="username", password = "password", dbname = "dbname", schemaname="schemaname")
   >>> con = get_connection(username="username", password = "password", dbname = "dbname", schemaname="schemaname")

You can provide defaults for the above parameters by creating special files.
To avoid typing your username and password directly into your python scripts, you can create a :code:`.odbc.ini` file in your home folder with the following structure:

::

    [nuvolos]
    uid = <username>
    pwd = <password>

To specify the database and schema, you can create a :code:`.dbpath` file in the working directory of your python script
with the contents

::

    "<db_name>"."<schema_name>"