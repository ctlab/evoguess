Sampling
========

Define sampling size.

Const sampling
--------------

Constant sample size.

.. code-block:: none

    'sampling': {
        'slug': 'sampling:const',
        'count': <number>,
        'order': <optional string>
    }

.. code-block:: none

    Orders: random, direct, reversed


Epsilon sampling
----------------

.. code-block:: none

    'sampling': {
        'slug': 'sampling:epsilon',
        'min': <number>,
        'max': <number>,
        'step': <number>,
        'epsilon': <number>,
        'delta': <optional number>,
        'order': <optional string>
    }


UP Steps sampling
-----------------

.. code-block:: none

    'sampling': {
        'slug': 'sampling:up_steps',
        'min': <number>,
        'steps': <number>,
        'order': <optional string>
    }