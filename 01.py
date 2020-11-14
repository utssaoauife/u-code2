#! /usr/bin/env python3

def solve(*args):
    return "#%02X%02X%02X" % (*[min(255, max(0, x)) for x in args],)

if __name__ == "__main__":
    t = int(input())
    for _ in range(t):
        print(solve(*(int(x) for x in input().split())))
