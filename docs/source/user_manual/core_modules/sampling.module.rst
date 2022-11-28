Sampling
========

Define sampling size.

Const sampling
--------------

Constant sample size.

.. code-block:: python

    from core.module.sampling import Const

    sampling = Sampling(
        value: int,
        split_into: int
    )


Epsilon sampling
----------------

.. code-block:: python

    from core.module.sampling import Epsilon

    sampling = Epsilon(
        step: int,
        epsilon: float,
        min_count: int,
        max_count: int,
        split_into: int,
        delta: float = 0.5
    )
