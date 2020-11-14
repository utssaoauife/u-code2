#! /usr/bin/env python3

from math import ceil, floor

def solve(a, b):
    return floor(round(b ** (1/3), 8)) - ceil(a ** (1/3)) + 1

if __name__ == "__main__":
    for _ in range(int(input())):
        print(solve(*(int(x) for x in input().split())))
