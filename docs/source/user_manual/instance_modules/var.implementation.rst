Var
===

Index
------

Реализация для создания обычной индексной переменной.

.. code-block:: none

    Index(index: <number>)

Domain
------

Реализация для создания виртуальной доменной именованной переменной **name**.
Домен определяется размером списка зависимых переменных **group**.

.. code-block:: none

    Domain(name: str, group: <list of numbers>)

Switch
------

Реализация для создания виртуальной переключаемой именованной переменной **name**.
Подставляемые constranints зависят от значений, принимаемой булевой функцией **op** на различных комбинациях входов зависимых булевых переменных **group**.

.. code-block:: none

    Switch(name: str, op: <function>, group: <list of numbers>)

Examples
--------

Примеры создания **Index**, **Domain** and **Switch** объектных переменных, и их влияние на решаемую кодировку, при подстановке значений.

.. code-block:: none

    from instance.module.variables.operation import xor
    from instance.module.variables.vars import Index, Domain, Switch

    index_var = Index(33)
    # if variable 33 equals 1, then add assumptions [33] to cnf
    # if variable 33 equals 0, then add assumptions [-33] to cnf

    switch_var = Switch('s1', xor, [3, 4])
    # if variable s1 equals 0, then add constraints [[3, -4], [-3, 4]] to cnf
    # if variable s1 equals 1, then add constraints [[3, 4], [-3, -4]] to cnf

    domain_var = Domain('d1', [1, 2, 3, 4, 5]) # domain equals 5
    # if variable d1 equals 1, then add assumptions [1, -2, -3, -4, -4] to cnf
    # if variable d1 equals 3, then add assumptions [-1, -2, 3, -4, -4] to cnf

