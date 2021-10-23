from prime import *

primes = [2, 3, 5, 7, 11, 13, 17]
composites = [4, 6, 8, 9, 10, 12, 14, 15, 16]


def test_basic():
    for i in primes:
        assert not bool(check_range(i))
    for i in composites:
        assert bool(check_range(i))
