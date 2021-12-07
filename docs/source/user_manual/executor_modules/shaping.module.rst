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

Divides tasks into **chunk_rate\*workers** equal parts.

.. code-block:: none

    'shaping': {
        'slug': 'shaping:chunks',
        'chunk_rate': <number>
    }

