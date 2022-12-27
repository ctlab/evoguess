Tuner (experimental)
====================

Runtime parameters tuner.

IBS tuner
---------

.. code-block:: none

    'selection': {
        'slug': 'tuner:ibs',
        'limit_key': <limit key>,
        'levels': <list of levels>,
        'save_mode': <optional bool>,
        'reset_after_increase': <optional bool>,
    }

.. code-block:: none

    level: {'bound': <limit value>, 'value': <ibs budget>},