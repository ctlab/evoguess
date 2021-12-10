Instance
========

.. code-block:: none

    'instance': {
        'slug': 'instance',
        'cnf': {
            'slug': 'cnf',
            'path': <relative to TEMPLATE_PATH from .env file>
        },
        'input_set': <interval>,
        'extra_set': <optional interval>
    }

Cipher
------

.. code-block:: none

    'instance': {
        'slug': 'cipher:stream',
        'cnf': {
            'slug': 'cnf',
            'path': <relative to TEMPLATE_PATH from .env file>
        },
        'supbs': <interval>
        'input_set': <interval>,
        'output_set': <interval>,
        'extra_set': <optional interval>
    }

Instance modules
----------------

.. toctree::
    :maxdepth: 1

    instance_modules/interval.module