#!/usr/bin/env python3
"""Calculates whether a number is prime or composite."""

from enum import Enum, auto
from math import floor, sqrt


def round_sqrt(num: int) -> int:
    """Computes the square root of the input `num`,
    and then rounds down to the nearest whole integer."""
    return floor(sqrt(num))


class Primality(Enum):
    """The possible variations a number may take in regards to primality.

    All natural numbers are either prime or composite. Once sufficiently large,
    however, it becomes extremely (exponentially) difficult to test all
    possible factorizations of a number.

    Therefore, for the test-number, n, it is possible to:

    1. Find a factor, f, such that n (mod f) === 0, proving n composite.
    2. Test all possible factors of n, and determine that none of these may factor n, proving
        n prime.
    3. Pass a lot of primality tests, but take a very long time to terminate, in which case
        assuming the number is prime may be optimal.
    """

    PRIME = auto()
    COMPOSITE = auto()
    UNKNOWN = auto()


class OrderedList(list):
    """A list extension class.
    Items may only be appended if they are larger than any other elements in the list.
    Due to this, only increasing number may be added, and prime numbers may be linearly
    tested without worry of skipping a number erroneously."""

    def max_elem(self):
        """Getter for the numerically largest item in this list."""
        # As long as sorted invariant is held:
        return self[-1] if self else -1
        # Otherwise, maximum may be calculated:
        # return max(*self)

    def append(self, item):
        """Appends the item to this list, only if it becomes the newly highest number."""
        if item > self.max_elem():
            super().append(item)

    def get_nums_below(self, ceiling: int) -> list[int]:
        """Getter for all the elements in this list that are comparatively less than
        some provided ceiling value."""
        idx = 0
        # Find where ceiling overtakes list elements, if it does
        while self[idx] <= ceiling:
            # TODO: If ceiling is never surpassed...
            idx += 1
        return self[:idx]


class PrimesCache:
    """A cache used for storing prime numbers, in order to test
    larger and larger numbers for primality."""

    def __init__(self):
        """Creates a new, initialized but empty cache which will hold prime numbers."""
        self._primes = OrderedList()

    @property
    def primes(self) -> OrderedList:
        """Gets the prime numbers contained in this cache."""
        return self._primes

    def __len__(self) -> int:
        """Number of prime integers cached."""
        return len(self.primes)

    def load_prime(self, val: int):
        """Loads the prime into the cache."""
        # Item is only appended to list if it is larger than the max-elem thus far, therefore
        # the item may NOT be present in the list yet.
        self.primes.append(val)

    def _possible_factors(self, val: int) -> list[int]:
        """Only numbers in the range [2, floor(square_root(val))]
        may be factors of an integer, 'val'."""
        return self.primes.get_nums_below(round_sqrt(val))

    def is_prime(self, val: int) -> bool:
        """Checks whether the number is prime or composite, based on known,
        smaller prime numbers.

        If the number is factorable by any prime number, then it is composite.
        Otherwise,
        it is prime.

        Composite factors need not be checked, because they will solely be redundant.
        For example, any number that is factorable by 4 (such as 8, 20, 40, etc.),
        will also be factorable by 4's factor(s), or 2.
        Thus, once the prime 2 has been cached, there is no need to check for
        any ancestors of the composite 4.

        Returns True if the number is prime, and False if it is composite."""
        return not any(val % p_num == 0 for p_num in self._possible_factors(val))

    def highest_tested(self) -> int:
        """Gets the highest number known to be tested, whether composite or prime.
        Any number less than the highest tested number must definitively know its primality."""
        # Items should be numerically sorted, so the last item is the maximum
        return self.primes.max_elem()


# Hard-coded prime numbers
SMALL_PRIME_NUMS = [
    2,
    3,
    5,
    7,
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    61,
    67,
    71,
    73,
    79,
    83,
    89,
    97,
]


class SmallPrimesCache(PrimesCache):
    """A cache composed of a bunch of hard-coded prime numbers, all less than 100."""

    def __init__(self):
        super().__init__()
        for num in SMALL_PRIME_NUMS:
            self.load_prime(num)

    def highest_tested(self) -> int:
        """Capped at 100, uncertainty begins after this point."""
        return 100


class DynamicPrimesCache(SmallPrimesCache):
    """A cache of prime numbers, which calculates the members in the list at runtime.
    The smaller, hard-coded cache is used as a starting point, and then the dynamic
    algorithm is able to elegantly take over.
    """

    def __init__(self):
        """Creates a new dynamic prime number cache,
        bootstrapping off of the explicitly encoded cache."""
        super().__init__()
        self._highest_tested = super().highest_tested()

    def highest_tested(self) -> int:
        """Overrides the highest tested number, to dynamically change."""
        return self._highest_tested

    def inc_highest_tested(self) -> int:
        """Increments the highest tested number by one; Gets the next number to test."""
        self._highest_tested += 1
        return self.highest_tested()

    def test_next(self) -> bool:
        """Tests the next numerically larger number for primality.
        If it is prime, then it will be stored in the cache prior to returning true.
        Otherwise, if it is composite, the internal counter will simply be updated,
        and false will be returned."""
        # Next highest value
        test_num = self.inc_highest_tested()
        if self.is_prime(test_num):
            self.load_prime(test_num)
            return True
        return False

    def is_prime(self, val: int) -> bool:
        """Checks if the argument number is prime.
        Ensures that at least as high as the value specified has been tested."""
        # Ensure the value requested has been tested, and its primality has been cached
        target_ceil = round_sqrt(val)
        while self.highest_tested() < target_ceil:
            _ = self.test_next()
        return super().is_prime(val)
