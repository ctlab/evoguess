Solver
=======

SAT-solver.

PySat solver
------------

.. code-block:: none

    'solver': {
        'slug': 'solver:pysat:<name>'
    }

.. code-block:: none

    Names: cd, g3, g4, lgl, mcb, mcm, mpl, mc, m22, mgh.

Native solver
-------------

Native solvers should be built in the appropriate directories.

.. code-block:: none

    'solver': {
        'slug': 'solver:native:<name>'
    }

.. code-block:: none

    Names: kissat


Linear solver
-------------

Linear solver should be built in the directory *<SOLVER_PATH>/linear/propagate* (SOLVER_PATH from .env file).

.. code-block:: none

    'solver': {
        'slug': 'solver:linear'
    }
