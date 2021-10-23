#!/usr/bin/env python3

from math import sqrt
from typing import Iterable
import argparse


def check_div(base: int, i: int) -> bool:
    """Checks whether the factor, i, evenly divides the base number provided."""
    return base % i == 0


def get_range(base: int, max_num: int = -1) -> Iterable[int]:
    """Getter for the range of possible factors of the base number supplied."""
    root = int(sqrt(base))
    if max_num >= 0:
        root = min(root, max_num)
    return range(2, root + 1)


def check_range(base: int, max_num: int = -1):
    """Checks all possible factors of the base number, through the maximum number argument.

    If any number evenly divides the base, then that number is returned.
    Otherwise, a false value is returned.
    """
    for val in get_range(base, max_num):
        if check_div(base, val):
            return val
    return False


def get_parser():
    parser = argparse.ArgumentParser(
        description="determine whether some number is (likely) prime or composite."
    )
    parser.add_argument(
        "number", metavar="NUM", type=int, help="the number to check for primality."
    )
    # parser.add_argument("--verbose", action="store_true", help="print more information")
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    test_num = args.number
    factor = check_range(test_num)
    if not factor:
        print(f"{test_num} appears to be prime!")
    else:
        print(f"{test_num} is divisible by {factor}")


if __name__ == "__main__":
    main()
