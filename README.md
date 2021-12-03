# EvoGuess

## About

EvoGuess is a Python framework for hardness estimation and decomposition set search. EvoGuess contains evolution
algorithm (μ, λ), (μ + λ) and genetic algorithm elitism for optimize estimation function.

EvoGuess has been used in experimental part of paper "Evaluating the Hardness of SAT Instances Using Evolutionary
Optimization Algorithms"

## Preparing

Install packages

```
pip3 install numpy
pip3 install pebble
pip3 install python-sat
pip3 install mpi4py (for MPI)
```

## Run

```
python3 main2.py <instance>
```

## MPI Run

EvoGuess supports distributed computing through Message Passing Interface ([MPI](https://www.mpi-forum.org/))
using [mpi4py library](https://mpi4py.readthedocs.io/).

```
mpiexec -n node_count python3 -m mpi4py.futures main.py <instance>
```

## Required Arguments

EvoGuess contains some cnf instances (*evoguess\instance\cnf\templates*) prepared for black-box optimization.<br/>
The CP2021 paper examined **pvs:4_7**, **bvs:4_7**, **bvp:4_7**, **sgen:6_150_1001**, **sgen:6_150_101** and
**sgen:6_150_200** instances.

* **instance**
    - **e0** – E0
    - **a5** – A5/1
    - **asg:sk_ks** – ASG (args: sk - input bits, ks - output bits)
    - **gr:v** – Grain (args: v - version)
    - **tr** – Trivium
    - **biv** – Bivium
    - **tr64** – Trivium 64/75
    - **tr96** – Trivium 96/100
    - **bvi:n_k** – BubbleVsInsert (args: n numbers of k bits)
    - **bvp:n_k** – BubbleVsPancake (args: n numbers of k bits)
    - **bvs:n_k** – BubbleVsSelection (args: n numbers of k bits)
    - **pvs:n_k** - PancakeVsSelection (args: n numbers of k bits)
    - **php:p_h** - PHP (args: p - pigeons, h - holes)
    - **sgen:v_n_seed** - SGEN (args: v - version, n variables, seed)

## Additional Arguments

* **-t** – Count of threads (**only using in main2.py**) (default: 4)
* **-v** – Verbosity for debug logs [0-4] (default: 3)
* **-o** - Logging directory (default: main)
* **-wt** – Walltime: hh:mm:ss (default: 24:00:00)
* **-a** – Optimisation algorithm, see **Black-box optimization algorithms** (default: 1+1)
* **-n** - Sampling function, see **Task sampling** (default: 1000)
* **-b** - Initial backdoor (default: all input variables, support enumerations "1 2 3 4 5" and ranges "1..5")

* **-s** – SAT-solver, see **Solvers** (default: g3)
* **-m** - Evaluated measure, see **Measure** (default: props)

## Black-box optimization algorithms

* **!** – Tabu Search
* **m,l** – Evolution strategy (μ, λ)
* **m+l** – Evolution strategy (μ + λ)
* **m^l** – Genetic algorithm: Elitism (m elites from l individuals)

## Task sampling

* **n** – Const sampling of n subtasks
* **mn:mx:step@epsilon**[d**delta**] – Dynamic sampling depending on epsilon value (mn - min size, mx max size, step -
  sampling step, epsilon, delta)

## Solvers

EvoGuess using [PySAT library](https://github.com/pysathq/pysat) for solving SAT-tasks.

* **cd**  – CaDiCaL
* **g3**  – Glucose 3.0
* **g4**  – Glucose 4.1
* **lgl** – Lingeling
* **mcb** – MapleLCMDistChronoBT
* **mcm** – MapleCM
* **mpl** – MapleSat
* **mc**  – Minicard 1.2
* **m22** – Minisat 2.2
* **mgh** – Minisat GitHub version

## Measure

While solving tasks SAT-solver counts several measures. To evaluate hardness EvoGuess can use one of this measure:

* **time** – Time
* **confs** – Conflicts
* **props** – Propagations

## Examples

Black-box optimization by evolution strategy (1+1) using 36 threads and 12 hours. SAT-solver Glucose 3, const sampling
500 subtasks,

```shell script
python3 main2.py pvs:7_4 -t 36 -wt 12:00:00 -v 3 -n 500 -s g3 -a 1+1
```

Black-box optimization by genetic algorithm elitism(2, 6) using node_count nodes 36 threads and 12 hours. SAT-solver
Glucose 3, dynamic sampling 100..500 subtasks with step 100, eps = 0.1, delta = 0.05,

```shell script
mpiexec -n node_count python3 -m mpi4py.futures main.py domain:8 -wt 12:00:00 -v 3 -n 100:500:100@0.1d0.05 -s cd -a 2^6
```
