Preliminaries
=============

You can skip the configuration file and import all components and modules manually.
This will allow you to write your own implementations for components and modules and use them.

.. code-block:: none

        # advanced.py

        algorithm = Elitism(
            awaited_count=2,
            size=8, elites=2,
            mutation=Doer(),
            selection=Roulette(),
            crossover=TwoPoint(),
            limit=WallTime('12:00:00'),
            method=Method(
                function=UPGuessAndDetermine(
                    max_n=30,
                    solver=Glucose3(),
                    measure=Propagations(),
                ),
                executor=ProcessExecutor(
                    workers=4,
                    shaping=Chunks(chunk_rate=4)
                ),
                sampling=Const(count=100)
            ),
            instance=Instance(
                input_set=Interval(start=1, length=3244),
                cnf=CNF(path='sorting/pancake_vs_selection/pancake_vs_selection_7_4.cnf'),
            ),
            output=JSONOut(path='test/pvs_7_4'),
        )
        backdoor = algorithm.instance.get_backdoor()
        solution = algorithm.start_from_backdoors(backdoor)