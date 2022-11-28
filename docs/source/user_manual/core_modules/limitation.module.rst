Limitation
==========

Limits the resources used by algorithms in the optimization process.

WallTime
--------

Limits execution time. *from_string* format: '<hours>:<minutes>:<seconds>'.

.. code-block:: python

    from core.module.limitation import WallTime

    limitation = WallTime(
        from_string: str
    )

Iteration
---------

Limits the number of algorithm iterations.

.. code-block:: python

    from core.module.limitation import Iteration

    limitation = Iteration(
        value: int
    )
