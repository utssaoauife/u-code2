#! /usr/bin/env python3

from math import sqrt

def largest_p_fac(n):
    while not n & 1: n >>= 1
    if n == 1: return 2

    sqrt_n = int(sqrt(n))

    for x in range(3, sqrt_n + 1, 2):
        if x > sqrt_n: break
        if not n % x:
            n //= x
            while not n % x:
                n //= x
            sqrt_n = int(sqrt(n))

    return n if n > 1 else x - 2


def solve(nums):
    nums = sorted(nums)
    numfacs = {}

    for n in nums:
        if n in numfacs:
            continue
        for num, fac in reversed(numfacs.items()):
            if not n % num:
                numfacs[n] = max(fac, largest_p_fac(n // num))
                break
        else:
            numfacs[n] = largest_p_fac(n)

    return max(reversed(numfacs), key=numfacs.get)


if __name__ == "__main__":
    t, p = map(int, input().split())
    for _ in range(t):
        print(solve(map(int, input().split(' '))))

