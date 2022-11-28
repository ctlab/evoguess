Instance
========

| Определяющие параметры:

* **encoding** -- Instance of `Encoding <instance_modules/encoding.module.html>`_ module.

.. code-block:: python

    from instance.impl import Instance

    instance = Instance(
        encoding: Encoding
    )

Stream Cipher
-------------

| Определяющие параметры:

* **encoding** -- Instance of `Encoding <instance_modules/encoding.module.html>`_ module.
* **input_set** -- Instance of `Variables <instance_modules/variables.module.html>`_ module.
* **output_set** -- Instance of Indexes in `Variables <instance_modules/variables.module.html>`_ module.
* **extra_set** -- Instance of `Variables <instance_modules/variables.module.html>`_ module.

.. code-block:: python

    from instance.impl import StreamCipher

    instance = StreamCipher(
        encoding: Encoding,
        input_set: Indexes,
        output_set: Variables,
        extra_set: Optional[Variables]
    )

Block Cipher
-------------

| Определяющие параметры:

* **encoding** -- Instance of `Encoding <instance_modules/encoding.module.html>`_ module.
* **input_set** -- Instance  of Indexes `Variables <instance_modules/variables.module.html>`_ module.
* **plain_set** -- Instance  of Indexes `Variables <instance_modules/variables.module.html>`_ module.
* **output_set** -- Instance of `Variables <instance_modules/variables.module.html>`_ module.
* **extra_set** -- Instance of `Variables <instance_modules/variables.module.html>`_ module.

.. code-block:: python

    from instance.impl import BlockCipher

    instance = BlockCipher(
        encoding: Encoding,
        input_set: Indexes,
        plain_set: Indexes,
        output_set: Variables,
        extra_set: Optional[Variables]
    )

Instance modules
----------------

.. toctree::
    :maxdepth: 1

    instance_modules/encoding.module
    instance_modules/variables.module