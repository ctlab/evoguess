.. EvoGuess documentation master file, created by sphinx-quickstart on Fri Dec  3 18:13:38 2021. You can adapt this file completely to your liking, but it should at least contain the root `toctree` directive.

Welcome to EvoGuess's documentation!
====================================

| Framework for hardness estimating of SAT instances by decomposition set searching.
| Some Boolean formula is estimated in the following way:

1. the algorithm **chooses** decomposition set of some variables of the Boolean formula;
2. the original formula is **splits** into a number of simpler formulas using chosen decomposition set;
3. the resulting simpler formulas are **solved** and statistics of measures are collected;
4. the hardness is **estimated** hardness using special function.

Now more about each stage.

Choosing
--------

Metaheuristic algorithms, in particular evolutionary ones, are used to choose decomposition sets.
While working algorithm builds new decomposition sets based on previously estimated decomposition sets.
Special functions are used to estimate them.

Splitting
---------

To split original formula into a number of simpler formulas, the values of variables from decomposition set are fixed.
Each fixed value of variable *x* splits the original formula in two: the case of the positive literal of *x* and the case of the negative literal *¬x*.
Since the number of simpler formulas exponentially depends on the size of the decomposition sets, the Monte Carlo method is used to generate a random sample of formulas of limited size.

Solving
-------

At this stage, the SAT solver processes the resulting set of simplified formulas.
Depending on the used evaluation function, the solver can operate in two modes: solving or propagating.
And also work with time limit or conflicts/propagations budget.
At the end of the solver's process, measures are collected for all formulas, which will be used to estimate the corresponding decomposition set.

Estimating
----------

| The measures collected in the previous step are used to calculate the estimation.
| For this one of the functions can be used:

1. **Guess-and-Determine** (G-a-D)
2. G-a-D based on **Inverse Backdoor Sets** (IBS), which proposed in [AAAI2018]_
3. G-a-D based on **ρ-backdoors**, which proposed in [AAAI2022]_

.. toctree::
    :maxdepth: 1
    :caption: Getting started

    getting_started/installation
    getting_started/how_use
    getting_started/configuration
    getting_started/citations

.. toctree::
    :maxdepth: 1
    :caption: User manual

    user_manual/algorithm
    user_manual/instance
    user_manual/executor
    user_manual/function
    user_manual/method
    user_manual/output
    user_manual/backdoors
    user_manual/example_configuration

.. toctree::
    :maxdepth: 1
    :caption: Advanced usage

    advanced_usage/preliminaries
    advanced_usage/algorithm.abstract
    advanced_usage/executor.abstract
    advanced_usage/function.abstract
    advanced_usage/output.abstract
