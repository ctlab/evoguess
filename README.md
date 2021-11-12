# EvoGuess

## Подготовка

Установка пакетов

```
pip3 install numpy
pip3 install python-sat
pip3 install python-dotenv
```

Установка EvoGuess

```
mkdir evoguess-fw && cd evoguess-fw
git clone git@github.com:alpavlenko/evoguess.git
git clone git@github.com:alpavlenko/evoguess_data.git
```

## Environment

Указать путь до папки **evoguess-fw** в `ROOT_PATH` в файле `.env`.

Проверить, что `MAIN_PATH` и `DATA_PATH` указывают на папки **evoguess** и **evoguess_data** соответственно.

## Запуск

Передать конфигурацию строкой в json-формате в качестве аргумента для `main.py`

```
python3 main.py <configuration json-string>
```

Задать конфигурацию внутри файла `main2.py`

```
python3 main2.py
```

## Конфигурация

```
{
    'algorithm': ...
    'instance': ...
    'method': ...
    'function': ...
    'executor': ...
    'backdoors': ...
    'output': ...
}
```

### 1. Алгоритм

#### 1.1. Абстракция `Evolution`

Асинхронная версия эволюционного алгоритма.<br>
Параметр ***awaited_count*** влияет на *степень асинхронности* алгоритма.
От **1** (полная **а**синхронность) до **lmbda** (полная синхронность, по умолчанию).
По сути, задает число точек, которого достаточно для обновления популяции.

##### 1.1.1. Реализация `(μ, λ)`

```
'algorithm': {
    'slug': 'evolution:comma',
    'mu': <number>,
    'lmbda': <number>,
    'limit': <module>,
    'mutation': <module>,
    'selection': <module>
}
```
Доступна только синхронная версия стратегии `(μ, λ)` (параметр ***awaited_count*** залочен в **lmbda**).

##### 1.1.2. Реализация `(μ + λ)`

```
'algorithm': {
    'slug': 'evolution:plus',
    'mu': <number>,
    'lmbda': <number>,
    'limit': <module>,
    'mutation': <module>,
    'selection': <module>,
    'awaited_count': <optional number, default: lmbda>
}
```

#### 1.2. Абстракция `Genetic`

Асинхронная версия генетического алгоритма.<br>
Про параметр ***awaited_count*** см. выше. 
Значение от **2** до **size - elites** (по умолчанию).

##### 1.2.1. Реализация `Elitism`

```
'algorithm': {
    'slug': 'genetic:elitism',
    'size': <number>,
    'elites': <number>,
    'limit': <module>,
    'mutation': <module>,
    'selection': <module>,
    'crossover': <module>,
    'awaited_count': <optional number>
}
```

#### 1.3. Реализация `Tabu Search`

Итеративная жадная версия tabu search с возвратами.

```
'algorithm': {
    'slug': 'iterative:tabu_search',
    'limit': <module>,
    'shuffle_seed': <optional number>
}
```

#### 1.4. Модули

##### 1.4.1. Ограничение ресурсов

###### 1.4.1.1. Ограничение `WallTime`

Ограничение по времени исполнения.

```
'limit': {
    'slug': 'limit:walltime',
    'value': <hours>:<minutes>:<seconds>
}
```

###### 1.4.1.2. Ограничение `Iteration`

Ограничение по числу итераций.

```
'limit': {
    'slug': 'limit:iteration',
    'value': <number>
}
```

##### 1.4.2. Оператор мутации

###### 1.4.2.1. `Uniform` mutation

Вероятность мутации каждого бита вектора из **n** элементов равна **scale/n** (по умолчанию **1/n**).

```
'mutation': {
    'slug': 'mutation:uniform',
    'seed': <optional number>,
    'scale': <optional float>
}
```

###### 1.4.2.2. `Doer` mutation

[comment]: <> (добавить ref)

```
'mutation': {
    'slug': 'mutation:doer',
    'seed': <optional number>,
    'beta': <optional number>
}
```

##### 1.4.3. Оператор селекции

###### 1.4.3.1. `Best` selection

Выбирает среди ***number_of_bests*** лучших особей.

```
'selection': {
    'slug': 'selection:best',
    'seed': <optional number>,
    'number_of_bests': <number>
}
```

###### 1.4.3.2. `Roulette` selection

Вероятность, того что особь будет выбрана обратно пропорционально зависит от значения её фитнеса.

```
'selection': {
    'slug': 'selection:roulette',
    'seed': <optional number>,
}
```

[comment]: <> (###### 1.4.3.3. `Tournament` selection &#40;**еще не реализовано**&#41;)

[comment]: <> (```)

[comment]: <> ('selection': {)

[comment]: <> (    'slug': 'selection:tournament',)

[comment]: <> (    'roundes': <number>)

[comment]: <> (})

[comment]: <> (```)

##### 1.4.4. Оператор скрещивания

###### 1.4.4.1. `One-point` crossover

```
'selection': {
    'slug': 'crossover:one-point',
    'seed': <optional number>,
}
```

###### 1.4.4.2. `Two-point` crossover

```
'selection': {
    'slug': 'crossover:two-point',
    'seed': <optional number>,
}
```

###### 1.4.4.3. `Uniform` crossover

Вероятность с которой биты будут поменяны местами ***prob*** (по умолчанию **0.2**).

```
'selection': {
    'slug': 'crossover:uniform',
    'seed': <optional number>,
    'prob': <optional float>
}
```

### 2. Instance

#### 2.1. Интерфейс `Instance`

```
'instance': {
    'slug': 'instance',
    'cnf': {
        'slug': 'cnf',
        'path': <относительно TEMPLATE_PATH из .env файла>
    },
    'input_set': {
        'slug': 'interval',
        'start': <number>,
        'length': <number>,
    }
}
```

[comment]: <> (#### 2.2. Интерфейс `Cipher` &#40;**еще не реализовано**&#41;)

[comment]: <> (```)

[comment]: <> ('instance': {)

[comment]: <> (    'slug': 'cipher:stream',)

[comment]: <> (    'cnf': ...)

[comment]: <> (    'input_set': ...)

[comment]: <> (    'output_set': {)

[comment]: <> (        'slug': 'interval',)

[comment]: <> (        'start': <number>,)

[comment]: <> (        'length': <number>,)

[comment]: <> (    })

[comment]: <> (})

[comment]: <> (```)

### 3. Method

Служит для связи всех остальных компонентов.

```
'method': {
    'slug': 'method',
    'sampling': <module>
}
```

#### 3.1. Модули

##### 3.1.1. Sampling

###### 3.1.1.1. `Const` sampling

Постоянный размер выборки.

```
'sampling': {
    'slug': 'sampling:const',
    'count': <number>,
    'order': <optional string>
}
```

Orders: `random`, `direct`, `reversed`.

###### 3.1.1.2. `Epsilon` sampling

```
'sampling': {
    'slug': 'sampling:epsilon',
    'min': <number>,
    'max': <number>,
    'step': <number>,
    'epsilon': <number>,
    'delta': <optional number>,
    'order': <optional string>
}
```

###### 3.1.1.3. `UP Steps` sampling

```
'sampling': {
    'slug': 'sampling:up_steps',
    'min': <number>,
    'steps': <number>,
    'order': <optional string>
}
```

### 4. Function

#### 4.1. Guess-and-determine function

```
'function': {
    'slug': 'function:gad',
    'solver': <module>,
    'measure': <module>
}
```

#### 4.2. Guess-and-determine function (Unit Propagation)

```
'function': {
    'slug': 'function:upgad',
    'solver': <module>,
    'measure': <module>
}
```

#### 4.3. Модули

##### 4.3.1. Solver

##### 4.3.1.1. `PySat` solver

```
'solver': {
    'slug': 'solver:pysat:<name>'
}
```

Names: `cd`, `g3`, `g4`, `lgl`, `mcb`, `mcm`, `mpl`, `mc`, `m22`, `mgh`.

##### 4.3.2. Measure

##### 4.3.2.1. `Time` measure

```
'measure': {
    'slug': 'measure:time'
}
```

##### 4.3.2.2. `Conflicts` measure

```
'measure': {
    'slug': 'measure:conflicts'
}
```

##### 4.3.2.3. `Propagations` measure

```
'measure': {
    'slug': 'measure:propagations'
}
```

##### 4.3.2.4. `Learned literals` measure

```
'measure': {
    'slug': 'measure:learned_literals'
}
```

### 5. Executor

#### 5.1. `Thread pool` executor

```
'executor': {
    'slug': 'executor:thread',
    'workers': <number>,
    'shaping': <module>
}
```

#### 5.2. `Process pool` executor

```
'executor': {
    'slug': 'executor:process',
    'workers': <number>,
    'shaping': <module>
}
```

#### 5.3. Модули

##### 5.3.1. Shaping

##### 5.3.1.1. `Single` shaping

Помещает всю выборку задач в задании на один поток/процесс.

```
'shaping': {
    'slug': 'shaping:single',
}
```

##### 5.3.1.2. `Chunks` shaping

Делит выборку задач на *chunk_rate\*workers* равных частей.

```
'shaping': {
    'slug': 'shaping:chunks',
    'chunk_rate': <number>
}
```

### 6. Output

#### 6.1. `JSON` output

```
'output': {
    'slug': 'output:json',
    'path': <относительно EXPERIMENT_PATH из .env файла>
}
```

### 7. Backdoors

```
'backdoors': [<backdoor>, ...]
```

#### 7.1. `Base` backdoor

Если параметр **_list** не указан, то в качестве набора переменных будет использоваться **input_set** текущего `Instance`

```
{
    'slug': 'backdoor:base',
    '_list': <optional number list>
}
```