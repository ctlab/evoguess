Evolution Algorithms
====================

An asynchronous version of an evolutionary algorithm.
The **awaited_count** parameter affects how much the algorithm is asynchronous.
From **1** (full asynchronous) to **lambda** (full synchronous, default).
Essentially, it sets the number of points that are sufficient to update the population.

.. code-block:: none

    'algorithm': {
        'slug': ...,
        'mu': <number>,
        'lmbda': <number>,
        'limit': <module>,
        'mutation': <module>,
        'selection': <module>,
        'tuner': <optional module>,
        'awaited_count': <optional number>,
    }

Strategy (μ, λ)
---------------

Only the synchronous version of the strategy (μ, λ) is available (the **awaited_count** parameter is always **lmbda**).

.. code-block:: none

    'slug': 'evolution:comma'


Strategy (μ + λ)
----------------

.. code-block:: none

    'slug': 'evolution:plus'