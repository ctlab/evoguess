Core
====

Ядро нужно для того чтобы объединить все модули в единое целое и настроить их логику работы.


Optimize
--------

| Процесс оптимизации зависит от следующих параметров:

* **space** -- Instance of `Space <core_modules/space.module.html>`_ module.
* **logger** -- Instance of Logger in `Output <output.html>`_ package.
* **executor** -- Instance of Executor in `Executor <executor.html>`_ package.
* **instance** -- Instance of Instance in `Instance <instance.html>`_ package. :)
* **sampling** -- Instance of `Sampling <core_modules/sampling.module.html>`_ module.
* **function** -- Instance of Function in `Function <function.html>`_ package.
* **algorithm** -- Instance of Algorithm in `Algorithm <algorithm.html>`_ package.
* **comparator** -- Instance of `Comparator <core_modules/comparator.module.html>`_ module.
* **limitation** -- Instance of `Limitation <core_modules/comparator.module.html>`_ module.
* **random_seed** -- Random seed для инициализации random state, которые используется для генерации случайно выборки задач.

.. code-block:: python

   from core.impl import Optimize

    solution = Optimize(
        space: Space,
        logger: Logger,
        executor: Executor,
        instance: Instance,
        sampling: Sampling,
        function: Function,
        algorithm: Algorithm,
        comparator: Comparator,
        limitation: Limitation,
        random_seed: Optional[int]
    ).launch()


Core modules
-------------

.. toctree::
    :maxdepth: 1

    core_modules/space.module
    core_modules/sampling.module
    core_modules/comparator.module
    core_modules/limitation.module