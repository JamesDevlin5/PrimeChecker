#!/usr/bin/env python3
"""An amalgamation of tests which may not definitively prove a number prime,
but will be able to prove a number non-prime, or composite.

These formulas are more rigorous than many other hueristics,
and permit the level of confidence in any of the algorithm's outputs to also be determined.

As always, with more data comes more confidence in the results.
These probabilitistic tests may be repeated with as much input data as possible, leading
to a more confident answer, but taking more time to compute."""

from . import util


class PredRes(ABC):
    """The variations a number may result in taking, regarding primality.

    All natural numbers are either prime or composite. Once sufficiently large,
    however, it becomes extremely (exponentially) difficult to test all
    possible factorizations of a number.

    Therefore, for the possibly prime test-number, n, it is possible to:

    1. Find a factor, f, such that n (mod f) === 0, proving n composite.
    2. Test all possible factors of n, and determine that none of these may factor n, proving
        n prime.
    3. Pass a lot of primality tests, but take a very long time to terminate, in which case
        assuming the number is prime may be optimal.
    """

    @abstractmethod
    def is_prime(self) -> bool:
        """True if the predicate's result is more likely prime than composite."""
        pass


class PrimeRes(PredRes):
    """Indicates that the tested number is definitely prime."""

    def is_prime(self) -> bool:
        return True


class MaybePrimeRes(PrimeRes):
    """Indicates that the tested number is most likely prime."""

    def __init__(self, num_tests: int):
        self._num_tests = num_tests

    @property
    def num_tests(self) -> int:
        """Gets the number of tests that were completed (successfully)
        prior to assuming that the test number was probably prime."""
        return self._num_tests


class CompositeRes(PredRes):
    """Indicates that the tested number was proven composite."""

    def __init__(self, witness: int):
        self._wit = witness

    @property
    def witness(self) -> int:
        """Gets the witness number associated with this result;
        the (randomly chosen, usually) integer which failed to satisfy some relation
        involving the test number, which is always (or almost always) satisfied by a prime number.

        This other, non-test number in the relation dis-proves the candidate's possible primality,
        indicating that it must be composite."""
        return self._wit

    def is_prime(self) -> bool:
        return False


class PrimeTest(ABC):
    """An object which encapsulates an entire primality test, determining whether the provided
    argument is prime or composite, or somewhere in the middle."""

    @abstractmethod
    def sample_num(self) -> int:
        """Gets a number to be used in a relation equality expression, determining primality.
        Should this number prove the test value composite, it will become a witness of such.

        Generally, this sample space will change with every test type, but the goal is to randomly pick
        one of the items from the sample to be used in a test."""
        pass

    @abstractmethod
    def is_prime(self, val: int) -> PredRes:
        """Evaluates the prime predicate test for the argument `val` integer."""
        pass


class FermatTest(PrimeTest):
    """An implementation of the Fermat primality test."""

    def is_prime(self, val: int) -> PredRes:
        """Given an integer *n*:

        - Choose some integer *a* that is coprime to *n*
        - Calculate a^(n - 1) (mod n):
            ==! 1   =>   *n* is definitely composite
            ==? 1   =>   *n* might be prime
        """


class WilsonsThm(PrimeTest):
    def is_prime(self, val: int) -> PredRes:
        """A natural number, n, is prime if & only if:

        (n - 1)! === -1 (mod n)
        """
        return (factorial(val - 1) + 1) % val == 0
