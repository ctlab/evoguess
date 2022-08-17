Shaping
=======

Chunk shaping.

Single shaping
--------------

Places all tasks in a job on one thread/process.

.. code-block:: none

    'shaping': {
        'slug': 'shaping:single',
    }

Chunks shaping
--------------

Divides all tasks into chunk with size **chunk_size**.

.. code-block:: none

    'shaping': {
        'slug': 'shaping:chunks',
        'chunk_size': <number>
    }

