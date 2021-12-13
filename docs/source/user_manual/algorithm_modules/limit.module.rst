Limit
=====

Limits the resources used by algorithms in the optimization process.

WallTime limit
--------------

Limits execution time.

.. code-block:: none

    'limit': {
        'slug': 'limit:walltime',
        'value': <hours>:<minutes>:<seconds>
    }

Iteration limit
---------------

Limits the number of algorithm iterations.

.. code-block:: none

    'limit': {
        'slug': 'limit:iteration',
        'value': <number>
    }
