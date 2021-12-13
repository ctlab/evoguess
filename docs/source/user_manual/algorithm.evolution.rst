Evolution Algorithms
====================

| An asynchronous version of an evolutionary algorithm.
| The **awaited_count** parameter affects how much the algorithm is asynchronous.
| From **1** (full asynchronous) to **population_size** (full synchronous, default).
| Essentially, it sets the number of points that are sufficient to update the population.

.. code-block:: none

    'algorithm': {
        'slug': ...,
        'limit': <module>,
        'mutation': <module>,
        'selection': <module>,
        'tuner': <optional module>,
        'awaited_count': <optional number>,
    }

Strategy (μ, λ)
---------------

Only the synchronous version of (μ, λ) strategy is available (the **awaited_count** parameter is always **lmbda**).

.. code-block:: none

    'algorithm': {
        'slug': 'evolution:comma'
        'mu': <number>,
        'lmbda': <number>,
        'limit': <module>,
        'mutation': <module>,
        'selection': <module>,
        'tuner': <optional module>,
        'awaited_count': <optional number>,
    }


Strategy (μ + λ)
----------------

For (μ + λ) strategy **population_size** is **lmbda**.

.. code-block:: none

    'algorithm': {
        'slug': 'evolution:plus'
        'mu': <number>,
        'lmbda': <number>,
        'limit': <module>,
        'mutation': <module>,
        'selection': <module>,
        'tuner': <optional module>,
        'awaited_count': <optional number>,
    }


Algorithm modules
-----------------

.. toctree::
    :maxdepth: 1

    algorithm_modules/limit.module
    algorithm_modules/mutation.module
    algorithm_modules/crossover.module
    algorithm_modules/selection.module
    algorithm_modules/tuner.module