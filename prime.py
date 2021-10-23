#!/usr/bin/env python3

from math import sqrt
from typing import Iterable, Union
import argparse


def check_div(base: int, i: int) -> bool:
    """Checks whether the factor, i, evenly divides the base number provided."""
    return base % i == 0


def get_range(base: int, max_num: int = -1, verbose: bool = False) -> Iterable[int]:
    """Getter for the range of possible factors of the base number supplied."""
    root = int(sqrt(base))
    min_elem = 2
    if max_num >= 0:
        root = min(root, max_num)
    if verbose:
        print(f"Testing numbers in range: [{min_elem}, {root}]")
    return range(min_elem, root + 1)


def check_range(
    base: int, max_num: int = -1, verbose: bool = False
) -> Union[int, bool]:
    """Checks all possible factors of the base number, through the maximum number argument.

    If any number evenly divides the base, then that number is returned.
    Otherwise, a false value is returned.
    """
    for val in get_range(base, max_num, verbose):
        if check_div(base, val):
            print(f"{base} is divisible by {val}")
            return val
        elif verbose:
            print(f"Tested {val}...")
    return False


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="determine whether some number is (likely) prime or composite."
    )
    parser.add_argument(
        "number", metavar="NUM", type=int, help="the number to check for primality."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="print more information"
    )
    return parser


def main():
    args = get_parser().parse_args()
    test_num = args.number
    factor = check_range(test_num, verbose=args.verbose)
    if not factor:
        print(f"{test_num} appears to be prime!")


if __name__ == "__main__":
    main()
