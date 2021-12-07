Instance
========

.. code-block:: none

    'instance': {
        'slug': 'instance',
        'cnf': {
            'slug': 'cnf',
            'path': <relative to TEMPLATE_PATH from .env file>
        },
        'input_set': {
            'slug': 'interval',
            'start': <number>,
            'length': <number>,
        }
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
        'supbs': <optional interval>
        'input_set': {
            'slug': 'interval',
            'start': <number>,
            'length': <number>,
        },
        'output_set': {
            'slug': 'interval',
            'start': <number>,
            'length': <number>,
        }
    }