Selection
=========

Selection operator.

Best selection
--------------

Selects the best individuals among the **number_of_bests**.

.. code-block:: none

    'selection': {
        'slug': 'selection:best',
        'seed': <optional number>,
        'number_of_bests': <number>
    }

Roulette selection
------------------

Probability that an individual will be selected is inversely related to the value of its fitness.

.. code-block:: none

    'selection': {
        'slug': 'selection:roulette',
        'seed': <optional number>
    }