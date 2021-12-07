Function
========

Guess-and-determine
-------------------

.. code-block:: none

    'function': {
        'slug': 'function:gad',
        'solver': <module>,
        'measure': <module>
    }

Guess-and-determine (Unit Propagation)
--------------------------------------

.. code-block:: none

    'function': {
        'slug': 'function:upgad',
        'solver': <module>,
        'measure': <module>
    }

Inverse Backdoor Sets
---------------------

Define only one of time_limit, conf_budget or prop_budget.

.. code-block:: none

    'function': {
        'slug': 'function:ibs',
        'solver': <module>,
        'measure': <module>,
        'time_limit': <float>,
        'conf_budget': <number>,
        'prop_budget': <number>,
    }

Function modules
----------------

.. toctree::
    :maxdepth: 1

    function_modules/solver.module
    function_modules/measure.module
