import json
import math


def try_int(string):
    try:
        return int(string)
    except ValueError:
        return string


def try_bool(string):
    return {
        'true': True,
        'false': False
    }.get(string.lower(), string)


def try_json(string):
    try:
        return json.loads(string)
    except json.decoder.JSONDecodeError:
        return string


chain_casters = [try_int, try_bool]


def chain_cast(string):
    for caster in chain_casters:
        casted = caster(string)
        if not isinstance(casted, str):
            return casted
    return string


def inf_none(arg):
    if arg is None:
        return float('inf')
    elif math.isinf(arg):
        return None

    return arg
