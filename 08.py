#! /usr/bin/env python3

from collections import Counter

def solve(s):
    diff = Counter([s.count(x) for x in set(s)])
    if len(diff) == 1:
        return "YES"
    elif len(diff) == 2:
        if min(diff.values()) == 1:
            if diff[1] == 1 or diff[2] == 1:
                # Only one character with a count of 1 or 2
                # you can remove all it's occurences
                return "YES"
            elif abs(int.__sub__(*diff)) <= 2 and diff[max(diff.keys())] == 1:
                # One character has a count one or two greater than the other characters
                # you can remove one/two of its occurences
                return "YES"
        elif min(diff.values()) == 2:
            if diff[1] == 2:
                # One character has only two occurences
                # You can remove both occurences
                return "YES"
            elif abs(int.__sub__(*diff)) == 1 and diff[max(diff.keys())] == 2:
                # Two characters have a count one greater than the other characters
                # you can remove one of each.
                return "YES"
    elif len(diff) == 3:
        a, b, c = sorted(diff)
        if a == c - b == diff[a] == diff[c] == 1:
            # e.g {1: 1, 13: 20, 14: 1}
            # you can remove a single of both the min and max
            return "YES"

    return "NO"


if __name__ == "__main__":
    for _ in range(int(input())):
        print(solve(input()))
