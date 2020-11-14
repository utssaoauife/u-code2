#! /usr/bin/env python3

def solve(ranked, player):
    ranked = sorted(ranked, reverse=True)
    ranks = []
    pos = len(ranked) - 1

    for score in player:
        for pos in range(pos, -1, -1):
            if score < ranked[pos]:
                ranks.append(pos+2)
                break
            elif score == ranked[pos]:
                ranks.append(pos+1)
                break
        else:
            ranks.append(1)

    return ranks

if __name__ == "__main__":
    n = int(input())
    ranked = {int(x) for x in input().split()}
    m = int(input())
    player = map(int, input().split())

    print(*solve(ranked, player), sep='\n')
