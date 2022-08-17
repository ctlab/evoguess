Instance
========

.. code-block:: none

    'instance': {
        'slug': 'instance',
        'encoding': <encoding module>,
        'search_set': <variables module>
    }

Stream Cipher
-------------

.. code-block:: none

    'instance': {
        'slug': 'cipher:stream',
        'encoding': <encoding module>,
        'input_set': <variables module>,
        'extra_set': <optional variables module>
        'output_set': <variables module>,
        'search_set': <variables module>,
    }

Block Cipher
-------------

.. code-block:: none

    'instance': {
        'slug': 'cipher:block',
        'encoding': <encoding module>,
        'input_set': <variables module>,
        'plain_set': <variables module>,
        'extra_set': <optional variables module>
        'output_set': <variables module>,
        'search_set': <variables module>,
    }

Instance modules
----------------

.. toctree::
    :maxdepth: 1

    instance_modules/encoding.module
    instance_modules/variables.module