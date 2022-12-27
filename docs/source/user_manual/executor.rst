Executor
========

Thread Executor
---------------

.. code-block:: none

    'executor': {
        'slug': 'executor:thread',
        'workers': <number>,
        'shaping': <module>
    }

Process Executor
----------------

.. code-block:: none

    'executor': {
        'slug': 'executor:process',
        'workers': <number>,
        'shaping': <module>
    }

MPI Executor
------------

.. code-block:: none

    'executor': {
        'slug': 'executor:mpi',
        'shaping': <module>
    }

MPI Thread Executor
-------------------

.. code-block:: none

    'executor': {
        'slug': 'executor:thread:mpi',
        'shaping': <module>
    }

MPI Process Executor
--------------------

.. code-block:: none

    'executor': {
        'slug': 'executor:process:mpi',
        'shaping': <module>
    }

Executor modules
----------------

.. toctree::
    :maxdepth: 1

    executor_modules/shaping.module