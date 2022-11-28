Variables
=========

| Модуль для указания списка переменных.
| Список переменных можно считать из файла, указав к нему путь в аргументе **from_file**.
| Также список переменных можно задать напрямую через аргумент **from_vars**. Этот аргумент принимает список объектных переменных реализующих интерфейс **Var**.

.. code-block:: python

    from instance.module.variables import Variables

    variables = Variables(
        from_file: str,
        from_vars: List[Var]
    )

.. toctree::
    :maxdepth: 1
    :caption: Подробнее о реализациях интерфейса Var

    var.implementation

Indexes
-------

| Реализация для создания списка переменных, используя их номера.
| Номера переменных можно указать с помощью строки через параметр **from_string**.
| Или через **from_iterable** с помощью любой iterable структуры языка python.

.. note::
    Создание через параметр **from_string** также поддерживает внутренние интервалы, например: '1 2 3..8 10'

.. code-block:: python

    from instance.module.variables import Indexes

    variables = Indexes(
        from_string: str,
        from_iterable: Iterable[int],
    )

Interval
--------

| Реализация для создания интервала переменных, начиная с аргумента **start** и длины **length**.
| Также интервал можно задать с помощью строки через аргумент **from_string** в формате **'<start>..<end>'**.

.. code-block:: python

    from instance.module.variables import Interval

    variables = Interval(
        start: int,
        length: int,
        from_string: str
    )

Backdoor
--------

| Реализация для создания списка переменных, который используется в алгоритмах оптимизации.
| Является надстройкой над обычным списком переменных, каждая из которых может быть "включена" или "выключена". Логика "включения" реализована через битовые маски.
| Также, как и реализация **Variables**, может задаваться через аргументы **from_file** или **from_vars**.

.. note::
    Backdoors automatically built in `Space <../core_modules/space.module.html>`_ module

.. code-block:: none

    from instance.module.variables import Backdoor

    backdoor = Backdoor(
        from_file: str,
        from_vars: List[Var]
    )

Examples
--------

1) Указание списка переменных из интервала [1, 64].

.. code-block:: python

    from instance.module.variables import Interval

    variables = Interval(start=1, length=64)
    # or
    variables = Interval(from_string='1..64')

2) Указание списка переменных, используя их номера.

.. code-block:: python

    from instance.module.variables import Indexes

    variables = Indexes(from_string='1..5 12 15 23..25')
    # or
    variables = Indexes(from_iterable=[1, 2, 3, 4, 5, 12, 15, 23, 24, 25])

3) Чтение списка объектных переменных из файла.

.. code-block:: python

    from instance.module.variables import Variables

    variables = Variables(from_file='./_variables/test_vars.json')
