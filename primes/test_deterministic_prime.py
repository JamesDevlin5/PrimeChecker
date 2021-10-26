from deterministic_prime import *


def test_hard():
    cache = DynamicPrimesCache()
    assert cache.is_prime(5881)
    assert not cache.is_prime(5882)
