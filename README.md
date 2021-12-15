# EvoGuess

Framework for decomposition set searching and hardness estimating of SAT instances.
Decomposition set searching is based on the optimization of the estimation value (or hardness, in some cases) of such sets.
Metaheuristic algorithms, in particular evolutionary ones, are used for optimization.

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

To use the EvoGuess in MPI mode, you also need to install:

```shell script
$ pip install mpi4py
```

### Environment

Create **.env** file using **create_env.sh** script

```shell script
$ cd evoguess
$ ./create_env_file.sh
```

## How use

Run **main.py** using configuration file.

```shell script
$ python3 main.py -f <configuration file>
```

Or use configuration json-string.

```shell script
$ python3 main.py -l <configuration json-string>
```

### MPI use

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