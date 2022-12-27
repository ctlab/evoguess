How use
=======

Run **main.py** using configuration file.

.. code-block:: console

    $ python3 main.py -f <configuration file>


Or use configuration json-string.

.. code-block:: console

    $ python3 main.py -l <configuration json-string>


MPI use
-------

The EvoGuess can be run in MPI mode as follows:

.. code-block:: console

    $ mpiexec -n <workers> -perhost <perhost> python3 -m mpi4py.futures main.py -f <configuration file>
