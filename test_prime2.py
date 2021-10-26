from prime2 import *


def test_hard():
    cache = DynamicPrimesCache()
    assert cache.is_prime(5881)
    assert not cache.is_prime(5882)
