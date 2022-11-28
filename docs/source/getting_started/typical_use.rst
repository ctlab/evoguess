Typical use
===========

TODO

How to MPI use
--------------

The EvoGuess can be run in MPI mode as follows:

.. code-block:: console

    $ mpiexec -n <workers> -perhost <perhost> python3 -m mpi4py.futures main.py


where **perhost** is MPI workers processes on one node, and **workers** is a total MPI workers processes on all dedicated nodes.