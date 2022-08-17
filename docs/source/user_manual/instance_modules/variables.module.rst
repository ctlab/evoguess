Variables
=========

| Модуль для указания списка переменных.
| Список переменных можно считать из файла, указав к нему путь в аргументе **from_file**.
| Также список переменных можно задать напрямую через аргумент **from_vars**. Этот аргумент принимает список объектных переменных реализующих интерфейс **Var**.

.. note::
    Путь к файлу необходимо указывать относительно пути **TEMPLATE_PATH**, который указан в конфигурационном файле **.env**.

.. code-block:: none

    '...': {
        'slug': 'variables',
        'from_file': <filepath>
        'from_vars': <list of Vars>,
    }

.. toctree::
    :maxdepth: 1
    :caption: Подобнее о реализациях интерфейса Var

    var.implementation

Interval
--------

| Реализация для создания интервала переменных, начиная с аргумента **start** и длины **length**.
| Также интервал можно задать с помощью строки через аргумент **from_string** в формате **'<start>..<end>'**.

.. code-block:: none

    '...': {
        'slug': 'variables:interval',
        'start': <number>,
        'length': <number>,
        'from_string': <string>
    }

Indexes
-------

| Реализация для создания списка переменных, используя их номера.
| Номера переменных можно указать с помощью строки через параметр **from_string**.
| Или через **from_iterable** с помощью любой iterable структуры языка python.

.. note::
    Создание через параметр **from_string** также поддерживает внутренние интервалы, например: '1 2 3..8 10'

.. code-block:: none

    '...': {
        'slug': 'variables:indexes',
        'from_string': <string>,
        'from_iterable': <list of numbers>
    }

Backdoor
--------

| Реализация для создания списка переменных, который используется в алгоритмах оптимизации.
| Является надстройкой над обычным списком переменных, каждая из которых может быть "включена" или "выключена". Логика "включения" реализована через битовые маски.
| Также, как и реализация **Variables**, может задаваться через аргументы **from_file** или **from_vars**.

.. note::
    Backdoors can be automatically built using *get_backdoor* method of **instance** object.

.. code-block:: none

    '...': {
        'slug': 'variables:backdoor',
        'from_file': <filepath>
        'from_vars': <list of Vars>,
    }

Examples
--------

1) Указание списка переменных из интервала [1, 64].

.. code-block:: none

    '...': {
        'slug': 'variables:interval',
        'start': 1, 'length': 64,
        # or
        'from_string': '1..64',
    }

2) Указание списка переменных, используя их номера.

.. code-block:: none

    '...': {
        'slug': 'variables:indexes',
        'from_string': '1..5 12 15 23..25'
        # or
        'from_iterable': [1, 2, 3, 4, 5, 12, 15, 23, 24, 25],
    }

3) Чтение списка объектных переменных из файла.

.. code-block:: none

    '...': {
        'slug': 'variables',
        'from_file': '_variables/test_vars.json'
    }

Итоговый путь к файлу: **f'{TEMPLATE_PATH}/_variables/test_vars.json'**