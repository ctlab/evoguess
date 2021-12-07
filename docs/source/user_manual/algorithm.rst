Algorithm
=========

.. toctree::
    :maxdepth: 1
    :caption: Evolution

    algorithm.evolution
    algorithm.genetic


Tabu Search
-----------

An iterative greedy version of tabu search with backtracks.

.. code-block:: none

    'algorithm': {
        'slug': 'iterative:tabu_search',
        'limit': <module>,
        'shuffle_seed': <optional number>
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