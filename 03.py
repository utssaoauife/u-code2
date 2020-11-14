#! /usr/bin/env python3

def solve(a):
    count = {i: a.count(i) for i in set(a)}
    s = sorted(count.keys())

    if len(s) == 1: return len(a)

    # Maximum possible length of counts is (2*(len(s)-2) + 2)
    # Hence removal of duplicates is uncessary
    # since it'll only be used to calculate a running max (later on)
    # which is much less costlier than membership tests (even for sets)
    # at each appending operation.
    counts = []
    
    for x, y, z in zip(s[:-2], s[1:-1], s[2:]):
        if y - x <= 2:
            counts.append(count[x] + count[y])
        if z - x == 2:
            counts.append(count[x] + count[y] + count[z])
    
    if s[-1] - s[-2] <= 2:
        counts.append(count[s[-2]] + count[s[-1]])

    # Max among summed counts and individual counts
    return max(counts + list(count.values()))

if __name__ == "__main__":
    n = input()
    print(solve([int(x) for x in input().split()]))
