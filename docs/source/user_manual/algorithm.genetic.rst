Genetic Algorithms
==================

An asynchronous version of the genetic algorithm.
The **awaited_count** parameter affects how much the algorithm is asynchronous.
From **2** (full asynchronous) to **size - elites** (full synchronous, default).


.. code-block:: none

    'algorithm': {
        'slug': ...,
        'size': <number>,
        'elites': <number>,
        'limit': <module>,
        'mutation': <module>,
        'crossover': <module>,
        'selection': <module>,
        'tuner': <optional module>,
        'awaited_count': <optional number>
    }

Elitism
-------

.. code-block:: none

    'slug': 'genetic:elitism'