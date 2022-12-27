Installation
============

At the moment, only manual installation is available.

First clone the repository:

.. code-block:: console

    $ git clone git@github.com:ctlab/evoguess.git

Dependencies
------------

Next check the list of python3 dependencies:

.. code-block:: console

    $ pip install numpy
    $ pip install python-sat
    $ pip install python-dotenv

To use the EvoGuess in MPI mode, you also need to install:

.. code-block:: console

    $ pip install mpi4py


Environment
-----------

Create **.env** file using **create_env.sh** script

.. code-block:: console

    $ cd evoguess
    $ ./create_env.sh

