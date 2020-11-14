#! /usr/bin/env python3

from math import gcd

def solve(a, b, N):
    """ Returns sum of multiples of a *or* b *below* N
    Uses formular for sum of an AP.
    """

    sum_ = 0

    # Number of multiples of x below N is (N-1 // x)
    # *below* N, hence the `N-1`
    n = (N-1) // a + 1;
    sum_ += (n * (n-1)*a) // 2;
    n = (N-1) // b + 1;
    sum_ += (n * (n-1)*b) // 2;

    # Multiples of "a and b", which are the multiples their LCM
    # have been included twice, hence their sum has to be subtracted once
    # to get the correct result for "a or b"
    c = a * b // gcd(a, b)  # LCM of a and b
    n = (N-1) // c + 1;
    sum_ -= (n * (n-1)*c) // 2;

    return sum_


if __name__ == "__main__":
    t = int(input())
    for _ in range(t):
        a, b, n = map(int, input().split(' '))
        print(int(solve(a, b, n)))
