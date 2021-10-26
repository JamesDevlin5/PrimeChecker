# Prime Checker

A program to determine whether a number is (likely) prime or non-prime.

## Definition

Natural Number
: The infinite, countable set `N`, composed of all positive, rational whole numbers. (*1*, *2*, *3*, *4*, ...)

[Prime Number](https://en.wikipedia.org/wiki/Prime_number)
: A natural number that is not a product of any two other smaller natural numbers.

## Testing Primality

- [Trial Division](https://en.wikipedia.org/wiki/Trial_division): tests whether *n* is a multiple of any integer between 2 and sqrt(*n*).
- [Wilson's Theorem](https://en.wikipedia.org/wiki/Wilson%27s_theorem): determines whether a number is *likely* prime or composite.
- [Miller-Rabin Test](https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test): determines whether a number is *likely* to be prime.
- [AKS Test](https://en.wikipedia.org/wiki/AKS_primality_test): determines whether a number is prime or composite, in polynomial time.

## Wilson's Theorem

A natural number, *n*, is a prime number **iff**:

The product of all positive numbers less than *n* is one less than a multiple of *n*.
<br>
That is, `(n - 1)!`, or `1 * 2 * 3 * ... * (n - 1)`, must satisfy the relation:

```
(n - 1)! === -1 (mod n)
```
<br>
Or, any number *n* is a prime number **if and only if** `(n - 1)! + 1` is divisible by *n*.

### Proof

<!-- TODO: Double Check Below -->

If *n* is a composite number, then it is divisible by some prime number *q*, where 2 <= *q* <= *n - 2*.

Assume the contradiction:

```
(n - 1)! === -1 (mod n)
```

The following cases arise:

1. If *n* may be factored by two numbers, *n* = *a* x *b*, where *a* != *b*, then both *a* and *b* will appear in the product *(n - 1)!*. Therefore, *(n - 1)!* will be divisible by *n*, and *n* must be composite.
1. If *n* has no such existing prime-factorization, then there must exist some prime number, *q* (*q > 2*), for which *n = q^2*. However, then both *q* and *2q* will be factors of *(n - 1)!*, and *n* must be composite.
1. So *n* is most likely a prime number.

