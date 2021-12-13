Mutation
========

In evolutionary and genetic algorithms, the mutation operator is used to modify the vector specifying the decomposition set (one to one).

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