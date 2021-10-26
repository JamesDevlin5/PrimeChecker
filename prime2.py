#!/usr/bin/env python3

from typing import Iterator
from abc import ABC, abstractmethod


class PrimeGen(ABC):
    """A class to facilitate the generation of unique, sequential prime numbers."""

    def __init__(self):
        self._idx = 0

    @abstractmethod
    def __iter__(self):
        """Coerces this generator into an iterator."""
        pass

    @abstractmethod
    def __next__(self) -> int:
        """Updates the numerical count of items processed thus far."""
        self._idx += 1

    @property
    def idx(self) -> int:
        """Getter for the index, or count of items produced thus far."""
        return self._idx


class KnownPrimesGen(PrimeGen):
    """A generator of prime numbers, via their static coding in the class."""

    # Hard-coded prime numbers
    nums = [
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

    def __iter__(self) -> Iterator[int]:
        return self

    def __next__(self) -> int:
        while self.idx < len(KnownPrimesGen.nums):
            yield KnownPrimesGen.nums[self.idx]
            next(super())
        raise StopIteration()


class NumTester:
    """A class which defines a predicate API, that checks whether a number can be proven composite,
    or is instead likely to be (or most definitely is) prime."""

    def is_prime(self, num: int) -> bool:
        """Checks whether the number argument is prime, true, or composite, false."""
        return False
