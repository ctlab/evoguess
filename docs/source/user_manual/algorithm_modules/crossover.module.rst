Crossover
=========

In evolutionary and genetic algorithms, the crossing operator is used to swap bits between two vectors specifying the corresponding decomposition sets.

Uniform crossover
-----------------

Each bit can be swapped with a probability of **prob** (default **0.2**).

.. code-block:: none

    'selection': {
        'slug': 'crossover:uniform',
        'seed': <optional number>,
        'prob': <optional float>
    }

One-point crossover
-------------------

.. code-block:: none

    'selection': {
        'slug': 'crossover:one-point',
        'seed': <optional number>,
    }

Two-point crossover
-------------------

.. code-block:: none

    'selection': {
        'slug': 'crossover:two-point',
        'seed': <optional number>,
    }