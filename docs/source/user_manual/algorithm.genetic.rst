Genetic Algorithms
==================

| An asynchronous version of the genetic algorithm.
| The **awaited_count** parameter affects how much the algorithm is asynchronous.
| From **2** (full asynchronous) to **population_size** (full synchronous, default).

.. code-block:: none

    'algorithm': {
        'slug': ...,
        'limit': <module>,
        'mutation': <module>,
        'crossover': <module>,
        'selection': <module>,
        'tuner': <optional module>,
        'awaited_count': <optional number>
    }

Elitism
-------

For elitism realisation **population_size** is **size - elites**.

.. code-block:: none

    'algorithm': {
        'slug': 'genetic:elitism',
        'size': <number>,
        'elites': <number>,
        'limit': <module>,
        'mutation': <module>,
        'crossover': <module>,
        'selection': <module>,
        'tuner': <optional module>,
        'awaited_count': <optional number>
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