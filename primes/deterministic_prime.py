#!/usr/bin/env python3
"""Calculates whether a number is prime or composite."""


def round_sqrt(num: int) -> int:
    """Computes the square root of the input `num`,
    and then rounds down to the nearest whole integer."""
    return floor(sqrt(num))


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
        # Find where ceiling overtakes list elements, if it does
        if self.max_elem() <= ceiling:
            # Ceiling is larger than all nums in list
            return self
        idx = 0
        while self[idx] <= ceiling:
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
        while self.highest_tested() <= target_ceil:
            _ = self.test_next()
        return super().is_prime(val)


class SieveOfEratosthenes(PrimesCache):
    """An implementation of the Sieve of Eratosthenes algorithm,
    which leverages *trail division* to determine all composite numbers up to a
    ceiling. Any numbers not in this set, below the ceiling, must therefore be prime."""

    def __init__(self, limit: int):
        """Creates a buffer for holding composites found."""
        super().__init__()
        # Empty set of composites (for faster inclusion/exclusion checking
        self._composites = set()
        # Current number, for which the factors are calculated and added to the set of composite numbers
        self._curr = 2
        self._setup(limit)

    @property
    def _curr_num():
        """The current number being processed; whose factors are being noted as composite."""
        return self._curr

    def _setup(self, ceil: int):
        """Initializes the repetitive process of:

        1. Ensure ceiling has not been surpassed
        2. If current item is not composite  =>  Load it as a prime
         -  Append all factors of the current prime number, up to the ceiling value
        3. If current item is composite      =>  Remove it from composites list
        """
        while self._curr_num <= ceil:
            if self._curr_num not in self._composites:
                # Not composite => register prime, & save composite factors
                self.load_prime(self._curr_num)
                # Start at prime * 2
                curr_factor = self._curr_num * 2
                while curr_factor <= ceil:
                    # Load factors
                    self._composites.add(curr_factor)
                    curr_factor += self._curr_num
            else:
                self._composites.remove(self._curr)
                # Any and all factors of composites are checked via primes
            self._curr += 1
        # Free resources
        self._composites = None

    def highest_tested(self) -> int:
        """The highest number tested is the externally-defined ceiling imposed during instantiation."""
        return self._curr_num
