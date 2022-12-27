from dotenv import dotenv_values

const = dotenv_values(".env")
MAIN_PATH = const['MAIN_PATH']
SOLVER_PATH = const['SOLVER_PATH']
TEMPLATE_PATH = const['TEMPLATE_PATH']
EXPERIMENT_PATH = const['EXPERIMENT_PATH']

__all__ = [
    'MAIN_PATH',
    'SOLVER_PATH',
    'TEMPLATE_PATH',
    'EXPERIMENT_PATH',
]
