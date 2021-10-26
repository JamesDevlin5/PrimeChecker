#!/usr/bin/env python3
"""A mathematical library module, containing functionality for calculating
the greatest-common-divisor of two (or more) numbers."""


class GCD(ABC):
    """Greatest Common Divisor, of two natural numbers *a* and *b*.
    The largest natural number that divides both *a* and *b* without leaving a remainder."""

    @abstractmethod
    def calculate(self, a: int, b: int) -> int:
        """Calculates the greatest common divisor shared by the two arguments."""
        pass

    def gcd_many(self, elems: list[int]) -> int:
        """Calculates the greatest common divisor of all integers supplied in the list.
        This is possible due to the fact that the GCD of three or more numbers equals the
        product of the prime factors common to all the numbers.

        In other words, if we consider the prime factorization of each input number,
        *a*, *b*, and *c*, such that:

        A = a1 * a2 * a3 * a4
        B = b1 * b2
        C = c1 * c2 * c3 * c4 * c5

        Then the greatest common divisor of these three must be shared by **ALL** permutations
        of inputs to the `gcd()` operation.

        > gcd(a, b, c) = gcd(a, gcd(b, c)) = gcd(gcd(a, b), c) = gcd(gcd(a, c), b)
        """
        if len(elems) == 0:
            # If no elements, then no divisor may be calculated
            return -1
        elif len(elems) == 1:
            # One element, implying n is the greatest divisor of n, shared with n
            return elems[0]
        curried_gcd = elems.pop()
        for elem in elems:
            curried_gcd = self.calculate(curried_gcd, elem)
        return curried_gcd


class Euclidean(GCD):
    """A step-wise method of determining the greatest shared factor."""

    def div_calculate(self, a: int, b: int) -> int:
        """Calculates the greatest-common-divisor of a and b via repetetive division."""
        while b != 0:
            # b: holds the most recently found remainder, r_k-1
            # a: holds the predecessor of b, r_k-2
            #
            a, b = b, a % b
            # tmp = b
            # b = a % b # equivalent to: r_k === r_k-2 (mod r_k-1)
            # a = tmp
        return a
        # If: negative inputs, or if the *modulo* function can return negative values,
        # the last line must be:
        # return abs(a)

    def sub_calculate(self, a: int, b: int) -> int:
        """Calculates the GCD of a and b via repeated subtraction instead of division
        (or modulo)."""
        while a != b:
            self.step_count += 1
            # *a* and *b* will converge on some shared factor, eventually...
            if a > b:
                a = a - b
            else:
                b = b - a
        # If: negative inputs are permitted, the last line must be:
        # return abs(a)
        return a

    def recursive_calculate(self, a: int, b: int) -> int:
        """The recursive GCD implementation, based on the equality of the GCDs of
        successive remainders, and the stopping condition: `gcd(r_n−1, 0) =? (r_n−1)."""
        if b == 0:
            return a
        else:
            return self.recursive_calculate(b, a % b)

    def calculate(self, a: int, b: int) -> int:
        """
        Each step begins with two nonnegative remainders *r_k−1* and *r_k−2*.
        Since the algorithm ensures that the remainders decrease steadily with every step,
        *r_k−1* is less than its predecessor *r_k−2*.

        The goal of the *k-th* step is to find a quotient, *q_k*, and a remainder, *r_k*,
        that satisfy the equation:

        `(r_k−2) = (q_k) x (r_k−1) + (r_k)`

        and that have 0 ≤ r_k < r_k−1.
        In other words, multiples of the smaller number, *r_k−1*,
        are subtracted from the larger number, *r_k−2*,
        until the remainder, *r_k*, is smaller than r_k−1.

        In the initial step (k = 0), the remainders, *r_k−2* and *r_k−1*,
        are set to be equal to *a* and *b*, the numbers for which the GCD is sought.
        In the next step (k = 1),
        the remainders equal b and the remainder *r_0* of the initial step, and so on.
        """
        # Defer call
        return self.recursive_calculate(a, b)


class LeastAbsRem:
    """Method of Least Absolute Remainders.
    Allows for calculating the gcd of negative numbers."""

    def calculate(self, a: int, b: int) -> int:
        """The quotient at each step is increased by one, *if* the resulting negative remainder is
        smaller in magnitude than the typical positive remainder.

        The previous revision of this algorithm assumed that the remainder was **strictly** getting smaller
        upon completing each step.

        E.g. the recurrence relation `r_k−2 = (q_k x r_k−1) + r_k` assumed that `|r_k−1| > r_k > 0` was true for all *r*.
        """
        pass


class Stein(GCD):
    """An implementation of Stein's algorithm (*the binary Euclidian algorithm*).

    The following identities are applied repeatedly until and GCD is determined:

    1. `gcd(0, v) == v`
    2. `gcd(2u, 2v) == 2 * gcd(u, v)`
    3. `gcd(2u, v) == gcd(u, v) if v is odd`
    4. `gcd(u, v) == gcd(|u - v|, min(u, v)) if u and v are both odd`

    Every 2 step iterations reduce at least one of the operands by a power of 2.
    Hence, this algorithm will require O(n), steps where n is the number
    of bits in the greater of the two argument numbers.

    However, this algorithm is asymptotically O(n^2) time, due to the fact that
    the (subtract and shift) bit-operators each take linear time for arbitrarily
    sized values.
    """

    def calculate(self, a: int, b: int) -> int:
        """Repetitive reduction in values, via simple and easy-to-prove identities."""
        # Base Cases: gcd(n, 0) == gcd(0, n) == n
        if a == 0:  # Rule 1
            return b
        if b == 0:  # Rule 1
            return a
        if a == b:
            return a

        a_even = bool(a % 2)
        b_even = bool(b % 2)

        if a_even and b_even:
            # Rule 2
            return self.calculate(a >> 1, b >> 1) << 1
        elif a_even:
            # Rule 3
            return self.calculate(a >> 1, b)
        elif b_even:
            # Rule 3
            return self.calculate(a, b >> 1)
        else:
            # Rule 4
            # if a >= b:
            #     return self.calculate(abs(a - b) >> 1, b)
            # else:
            #     return self.calculate(a, abs(b - a) >> 1)
            return self.calculate(abs(a - b), min(a, b))


class CoprimePred:
    """A predicate which tests whether two numbers, *a* and *b*, are co-prime.
    *a* and *b* will be co-prime **if & only if** `gcd(a, b) == 1`.

    > The numerator and denominator of any *reduced* fraction are co-prime.
        Otherwise, the common factor could be extracted and the fraction reduced.
    """

    pass
