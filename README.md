**The package is deprecated in favor of https://github.com/aimclub/evoguess-ai**

# EvoGuess

Framework for finding decomposition sets and estimating hardness of SAT instances.
The search for decomposition sets is realized via the optimization of the special 
pseudo-Boolean black-box functions that estimate the hardness of the decomposition 
corresponding to the employed decomposition method and the considered set. To
optimize the value of such functions the framework uses metaheuristic algorithms, 
in particular, the evolutionary ones.

## Installation

At the moment, only manual installation is available.

```shell script
$ git clone git@github.com:ctlab/evoguess.git
```

### Dependencies

```shell script
$ pip install numpy
$ pip install python-sat
$ pip install python-dotenv
```

To use EvoGuess in MPI mode, you also need to install:

```shell script
$ pip install mpi4py
```

### Environment

Create **.env** file using **create_env.sh** script

```shell script
$ cd evoguess
$ ./create_env.sh
```

## How to use

Run **main.py** using configuration file.

```shell script
$ python3 main.py -f <configuration file>
```

Or use configuration json-string.

```shell script
$ python3 main.py -l <configuration json-string>
```

### MPI mode

The EvoGuess can be run in MPI mode as follows:

```shell script
$ mpiexec -n <workers> -perhost <perhost> python3 -m mpi4py.futures main.py -f <configuration file>
```

### Example

Run on example configuration **config.json**.

```shell script
$ python3 main.py -f config.json
```

## Documentation

Documentation is available [here](https://evoguess.readthedocs.io/) and includes installation instructions, base and advanced usage manual.
