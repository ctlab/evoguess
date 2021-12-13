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

### How use

Run **main.py** using configuration file.

```
$ python3 main.py -f <configuration file>
```

Or use configuration json-string.

```
$ python3 main.py -l <configuration json-string>
```

### MPI use

The EvoGuess can be run in MPI mode as follows:

```
$ mpiexec -n <workers> -perhost <perhost> python3 -m mpi4py.futures main.py -f <configuration file>
```

### Example

Run on standard configuration **config.json**

```
$ python3 main.py -f config.json
```

### Documentation

Documentation is available [here](https://evoguess.readthedocs.io/) and includes installation instructions, base and advanced usage manual.