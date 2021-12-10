# EvoGuess

EvoGuess is a python framework for hardness estimating of SAT instances by decomposition set searching.

### Installation

At the moment, only manual installation is available.

```
$ mkdir evoguess-fw && cd evoguess-fw
$ git clone git@github.com:ctlab/evoguess.git
$ git clone git@github.com:alpavlenko/evoguess_data.git
```

### Dependencies

```
$ pip install numpy
$ pip install python-sat
$ pip install python-dotenv
```

To use the EvoGuess in MPI mode, you also need to install:

```
$ pip install mpi4py
```

### Environment

Create **.env** file using **create_env_file.sh** script

```
$ ./create_env_file.sh
```

### Documentation

Documentation is available [here](https://evoguess.readthedocs.io/) and includes installation instructions, base and advanced usage manual.