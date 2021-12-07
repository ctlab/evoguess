Mutation
========

Mutation operator.

Uniform mutation
----------------

The probability of mutation for each bit of a vector of **n** elements is **scale/n** (default **1/n**).

.. code-block:: none

    'mutation': {
        'slug': 'mutation:uniform',
        'seed': <optional number>,
        'scale': <optional float>
    }

Doer mutation
-------------

.. code-block:: none

    'mutation': {
        'slug': 'mutation:doer',
        'seed': <optional number>,
        'beta': <optional number>
    }