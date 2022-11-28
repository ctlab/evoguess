Encoding
========

| Модуль в котором задается исследуемая задача.
| Кодировку можно считать из файла, указав к нему путь в аргументе **from_file**.

CNF
---

| Реализация для кодировок в конъюнктивной нормальной форме (КНФ).
| Кодировку можно считать из файла **или** задать с помощью списка **from_clauses**.

.. code-block:: python

    from instance.module.encoding import CNF

    encoding = CNF(
        from_file: Optional[str],
        from_clauses: Optional[Clauses]
    )

CNF+
----

| Реализация для кодировок CNF+, that extends CNF to include cardinality constraints.
| Кодировку можно считать из файла **или** задать с помощью списка **from_clauses** и **from_atmosts**.

.. code-block:: python

    from instance.module.encoding import CNFP

    encoding = CNFP(
        from_file: Optional[str],
        from_clauses: Optional[Clauses]
        from_atmosts: Optional[Atmosts]
    )

