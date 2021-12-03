import warnings

from copy import copy
from math import log2, ceil

from numpy import count_nonzero
from numpy.random.mtrand import RandomState


def get_values(variables, **kwargs):
    if len(variables) == 0: return []
    if 'solution' in kwargs:
        solution = kwargs['solution']
        if len(solution) < variables[-1]:
            raise Exception('Solution has too few variables: %d' % len(solution))

        return [solution[x - 1] for x in variables]
    else:
        random_state = kwargs['rs'] if 'rs' in kwargs else RandomState()
        values = random_state.randint(2, size=len(variables))
        return [x if values[i] else -x for i, x in enumerate(variables)]


class Backdoor:
    type = 1

    # overridden methods
    def __init__(self, base, _list=()):
        self.base = base
        self.list = sorted(set(_list))
        self.length = len(self.list)
        self.mask = [True] * self.length

        assert len(self.list) > 0, 'Empty backdoor'
        assert self.list[0] >= 0, 'Backdoor contains negative numbers'
        if len(_list) != self.length:
            warnings.warn('Repeating variables in backdoor', Warning)

    def __str__(self):
        if len(self) == 0:
            return '[](0)'

        def itos(il):
            if il[1] - il[0] > 2:
                return '%s..%s' % (il[0], il[1])
            else:
                return ' '.join(map(str, range(il[0], il[1] + 1)))

        variables = self.snapshot()
        s, interval = '[', [variables[0], variables[0]]
        for i in range(1, len(variables)):
            if variables[i] - interval[1] == 1:
                interval[1] = variables[i]
            else:
                s += itos(interval) + ' '
                interval = [variables[i], variables[i]]
        return ''.join([s, itos(interval), '](%d)' % len(variables)])

    def __len__(self):
        return count_nonzero(self.mask)

    def __copy__(self):
        return self.get_copy(self.mask)

    def __iter__(self):
        for i in range(self.length):
            if self.mask[i]:
                yield self.list[i]

    def __contains__(self, item):
        return item in self.snapshot()

    def __hash__(self):
        return hash(tuple(self.snapshot()))

    # mask
    def _set_mask(self, mask):
        if len(mask) > self.length:
            self.mask = mask[:self.length]
        else:
            delta = self.length - len(mask)
            self.mask = mask + [False] * delta
        return self

    def get_mask(self):
        return copy(self.mask)

    def get_copy(self, mask):
        backdoor = Backdoor(self.base, self.list)
        return backdoor._set_mask(mask)

    def reset(self):
        self._set_mask([True] * self.length)

    # main
    def get_bases(self):
        return [self.base] * len(self)

    def task_count(self):
        return self.base ** len(self)

    def real_task_count(self):
        return self.task_count()

    def get_masks(self):
        return [(2 ** self.base - 1) << 1] * len(self)

    def get_mappers(self):
        return [list(range(1, self.base + 1))] * len(self)

    def snapshot(self):
        return [x for (i, x) in enumerate(self.list) if self.mask[i]]

    @staticmethod
    def parse(base, line):
        variables = []
        if len(line) > 0:
            for lit in line.split(' '):
                if '..' in lit:
                    var = lit.split('..')
                    variables.extend(range(int(var[0]), int(var[1]) + 1))
                else:
                    variables.append(int(lit))

        return Backdoor(base, variables)

    @staticmethod
    def empty(base):
        return Backdoor(base)


__all__ = [
    'Backdoor',
    'get_values'
]


if __name__ == '__main__':
    bd = Backdoor.parse(2, '9 10 16 23 48 53 55 56 59..63 65 69..71 75 82 85 90 96 104 108 120 121 124 131 139 144 146 153 159..161 165 168 171 175 179 180 190 192 194 201 202 205 210 213 215 217 219 223 225 231 232 239 241 246 251 253 259 261 264 266 272 274 279 283 284 293 296 311 313 316 324 333 336 337 347 352 365 368 373 376 380 386 387 395..398 402 404 407 411 414 420 422..424 428 432 436 441 442 446 460 465 467 469 476 477 479 483 485 490 497 501 508 514 519 528 532 534 537 538 540 541 544 551 553 555 565 566 570 572 573 576 578 580 582 594 597 599 607 618 623 624 630 634 646 652 654 665 669 671 672 674 679 683 692 709 719 724 726 740 743 746 759 766 772 782 790 793 794 799 805 821 826 832 837 838 842 848 851 860 866 868 874 876 880 890 894 902 906 910 919 920 924 948 950 954 968 971 978 980 982 988 1000 1005 1006 1008 1009 1011 1012 1026 1027 1035 1042 1044 1054 1059 1060 1066 1077..1079 1093 1106 1124 1130 1131 1133 1136 1138 1140 1142 1144 1145 1154 1164 1165 1168 1169 1172 1182 1189 1190 1193 1201 1202 1210 1211 1213 1216 1217 1229 1230 1232 1234 1237 1241 1243 1245 1249 1254 1255 1257 1258 1261 1264 1272 1274 1277 1290 1292 1293 1298..1300 1305 1306 1309 1315 1336 1337 1347 1353 1369 1370 1377 1380 1389..1391 1393 1396..1398 1406..1408 1418 1429 1432 1438 1445 1450 1454..1456 1459 1464 1469 1470 1473 1481 1492 1500 1507 1509 1511 1522 1524 1533 1536 1538 1541 1544 1548 1553 1562 1567 1568 1571 1573 1577 1581 1588 1592..1594 1600 1602 1604 1608 1617 1622 1628 1633 1637 1638 1641 1650 1654 1656 1659 1661 1665 1670 1676 1681 1684 1687 1691 1692 1697 1710 1712 1724 1729 1734 1736..1738 1740 1741 1747 1748 1751 1752 1755 1762 1768 1772 1777 1784 1787 1788 1822 1825 1828 1842 1858 1859 1866 1870 1873..1875 1882 1886 1899..1901 1906 1912 1923 1925 1934 1938 1941 1946 1951 1957 1963 1964 1969 1978 1982 1983 1990 1992 1995 2009 2013 2021 2024 2026 2034 2037 2038 2041 2048 2056 2059 2063 2082 2084 2091 2098 2104 2114 2122 2123 2126 2137 2138 2143 2145 2146 2148 2150 2161..2164 2173 2185 2191 2193 2194 2204 2205 2215 2221 2225 2227 2229 2230 2232 2233 2236 2238..2240 2248 2253 2263 2267 2273 2274 2282 2290 2292 2296 2298 2301 2303 2309 2324 2328 2329 2333 2334 2342 2351 2356 2362 2363 2378 2380 2383 2384 2386..2388 2392 2393 2398 2403 2406 2416 2419 2424 2428 2433..2435 2444 2448 2457 2458 2464 2466 2477 2478 2481 2483 2494 2498 2506 2517 2518 2521 2533 2535 2536 2544 2568 2569 2575 2576 2582 2587 2590 2594 2598 2606 2611..2613 2616 2624 2635 2640 2643 2651 2654 2680 2682 2692 2693 2695 2706 2721 2724 2726..2728 2730 2738 2744 2748 2750 2754 2755 2767 2771 2773 2774 2776 2781 2784 2785 2790 2795 2797 2799 2803 2805 2806 2808 2816 2817 2821..2823 2828 2833 2853 2861 2862 2867 2873 2875 2877 2878 2900 2902 2904 2909 2913 2914 2939 2946 2951 2958..2960 2972 2975..2977 2985 2988 2992..2994 2998 3003 3006 3018 3023 3024 3026 3031 3038 3040 3043 3047 3050 3061 3066 3069 3072 3075 3077 3083 3086 3090 3095 3096 3105 3107 3109 3110 3114 3121 3125 3137 3141 3147 3148 3165 3166 3170 3173 3174 3178 3183 3189 3194 3195 3206 3213 3214 3217 3221..3223 3226 3232 3236 3241')
    print(len(bd))