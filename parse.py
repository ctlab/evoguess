import re
import json
import tarfile
from os.path import join

from output.parser.impl.base import BaseParser
from structure.data.individual_top import IndividualsTop

pvs_main_path = './output/_main_logs/pancake_vs_selection'

if __name__ == '__main__':
    cache = {}
    bp = BaseParser()
    top = IndividualsTop()
    family, run = '7x4', '2021.12.03_15:06:45-2021.12.03_15:11:48'

    log_path = join(pvs_main_path, family, run)
    its = bp.parse(log_path)

    for it in its:
        for ind in it:
            key = str(ind.backdoor)
            cache[key] = ind.value
            top.check(ind)

    for ind in top.list():
        print(ind)
        values = [case[3]['propagations'] for case in ind.get('cases')]
        print(f'Ex: {round(sum(values) / len(values))} propagations\n')
