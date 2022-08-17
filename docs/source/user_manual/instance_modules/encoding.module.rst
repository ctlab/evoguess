Encoding
========

| Модуль в котором задается исследуемая задача.
| Кодировку можно считать из файла, указав к нему путь в аргументе **from_file**.

.. note::
    Путь к файлу необходимо указывать относительно пути **TEMPLATE_PATH**, который указан в конфигурационном файле **.env**.

CNF
---

| Реализация для кодировок в конъюнктивной нормальной форме (КНФ).
| Кодировку можно считать из файла **или** задать с помощью списка **clauses**.

.. code-block:: none

    'encoding': {
        'slug': 'encoding:cnf',
        'from_file': <filepath>
        'from_clauses': <list of Clauses>
    }

CNF+
----

| Реализация для кодировок CNF+, that extends CNF to include cardinality constraints.
| Кодировку можно считать из файла **или** задать с помощью списка **clauses** и **atmosts**.

.. code-block:: none

    'encoding': {
        'slug': 'encoding:cnf+',
        'from_file': <filepath>
        'from_atmosts': <list of Atmosts>,
        'from_clauses': <list of Clauses>,
    }


Examples
--------

1) Указание кодировки для потокового шифра A5_1 с помощью файла.

.. code-block:: none

    'encoding': {
        'slug': 'encoding:cnf',
        'from_file': 'cipher/stream/a5_1.cnf'
    }

Итоговый путь к файлу: **f'{TEMPLATE_PATH}/cipher/stream/a5_1.cnf'**

2) Указание кодировки через список clauses.

.. code-block:: none

    'encoding': {
        'slug': 'encoding:cnf',
        'from_clauses': [
            [1, 2, 3],
            [1, -2, 3],
            [-1, -2, 3]
        ],
    }
