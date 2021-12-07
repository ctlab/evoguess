How use
=======

Run **main.py** using configuration file.

.. code-block:: console

    $ python3 main.py -f <configuration file>


Or use configuration json-string.

.. code-block:: console

    $ python3 main.py -l <configuration json-string>

You can also set the configuration inside the **main2.py** file and run it.

.. code-block:: console

    $ python3 main2.py

MPI use
-------

The EvoGuess can be run in MPI mode as follows: (also works with **main.py**)

.. code-block:: console

    $ mpiexec -n <workers> -perhost <perhost> python3 -m mpi4py.futures main2.py
