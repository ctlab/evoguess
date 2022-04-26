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
        'slug': 'function:up_gad',
        'solver': <module>,
        'measure': <module>
    }

Inverse Backdoor Sets
---------------------

Define only one of **time_limit**, **conf_budget** or **prop_budget**.
Default value of **min_xi** is **0**. Backdoors with **xi < min_xi** will be ignored.

.. code-block:: none

    'function': {
        'slug': 'function:ibs',
        'solver': <module>,
        'measure': <module>,
        'time_limit': <float>,
        'conf_budget': <number>,
        'prop_budget': <number>,
        'min_xi': <optional float>,
    }

Linear Inverse Backdoor Sets
---------------------

**Works only with linear solver and time measure!**

Default value of **min_p** is **0**. Backdoors with **p < min_p** will be ignored.

.. code-block:: none

    'function': {
        'slug': 'function:ibs',
        'solver': <module>,
        'measure': <module>,
        'min_p': <optional float>,
    }

Function modules
----------------

.. toctree::
    :maxdepth: 1

    function_modules/solver.module
    function_modules/measure.module
