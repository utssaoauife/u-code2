#! /usr/bin/env python3

def total_squares(n: int, pieces: list, positions: list):
    hori_vert = (n-1) * 2
    dia_r_up = lambda r, c: min(n - c, n - r)
    dia_r_dn = lambda r, c: min(n - c, r - 1)
    dia_l_up = lambda r, c: min(c - 1, n - r)
    dia_l_dn = lambda r, c: min(c - 1, r - 1)

    max_squares = {'q': lambda r, c: (hori_vert
                                        + dia_r_up(r, c) + dia_r_dn(r, c)
                                        + dia_l_up(r, c) + dia_l_dn(r, c)),
                    'b': lambda r, c: (dia_r_up(r, c) + dia_r_dn(r, c)
                                        + dia_l_up(r, c) + dia_l_dn(r, c)),
                    'r': lambda r, c: hori_vert
                    }

    return sum([max_squares[piece](*pos) for piece, pos in zip(pieces, positions)])

def solve1(n: int, piece: str, r_p: int, c_p: int, obstacles: bytearray):
    """ Traverse pieces' paths and check for nearest obstacle
    using a (1 x N**2) bytearray. """

    # (x, y)
    hor_vert = ((0, 1), (1, 0), (0, -1), (-1, 0))  # Up, right, down, left
    diag = ((1, 1), (-1, -1), (1, -1), (-1, 1))
    moves = {'q': hor_vert + diag, 'b': diag, 'r': hor_vert}

    r_p -= 1
    c_p -= 1
    squares = 0
    for x, y in moves[piece]:
        r, c = r_p + y, c_p + x
        while 0 <= r < n and 0 <= c < n and obstacles[n*(r) + c]:
            r += y
            c += x

        squares += (min((r - r_p)*y - 1, (c - c_p)*x - 1) if x and y
                    else (c - c_p)*x - 1 if x else (r - r_p)*y - 1)

    return squares


def solve2(n: int, piece: str, r_p: int, c_p: int, obstacles: set):
    """ Loop over obstacles and check for nearest to the piece in each direction. """

    # Initial closest obstacles (board edges)
    up = right = r_up = l_up = n + 1  # using row for diagonals, hence n+1 (up)
    down = left = r_down = l_down = 0  # using row for diagonals, hence 0 (down)

    obstacles.remove((r_p, c_p))

    if piece == 'q':
        for r, c in obstacles:
            if c == c_p and r > r_p: up = min(up, r)
            elif c == c_p and r < r_p: down = max(down, r)
            elif r == r_p and c < c_p: left = max(left, c)
            elif r == r_p and c > c_p: right = min(right, c)
            elif r < r_p and c < c_p and r_p-r == c_p-c: l_down = max(l_down, r)
            elif r < r_p and c > c_p and r_p-r == c-c_p: r_down = max(r_down, r)
            elif r > r_p and c < c_p and r-r_p == c_p-c: l_up = min(l_up, r)
            elif r > r_p and c > c_p and r-r_p == c-c_p: r_up = min(r_up, r)
    elif piece == 'b':
        for r, c in obstacles:
            if r < r_p and c < c_p and r_p-r == c_p-c: l_down = max(l_down, r)
            elif r < r_p and c > c_p and r_p-r == c-c_p: r_down = max(r_down, r)
            elif r > r_p and c < c_p and r-r_p == c_p-c: l_up = min(l_up, r)
            elif r > r_p and c > c_p and r-r_p == c-c_p: r_up = min(r_up, r)
    elif piece == 'r':
        for r, c in obstacles:
            if c == c_p and r > r_p: up = min(up, r)
            elif c == c_p and r < r_p: down = max(down, r)
            elif r == r_p and c < c_p: left = max(left, c)
            elif r == r_p and c > c_p: right = min(right, c)

    squares = 0
    if piece in ('q', 'r'):
        squares += ((up - r_p - 1) + (r_p - down - 1)
                    + (right - c_p - 1) + (c_p - left - 1))
    if piece in ('q', 'b'):
        # For the diagonals, when there's no obstacle,
        # the correct number of squares is the minimum distance
        # to either egde of the board
        squares += (min(r_up-r_p, n+1-c_p) - 1 + min(r_p-r_down, n+1-c_p) - 1
                    + min(l_up-r_p, c_p) - 1 + min(r_p-l_down, c_p) - 1)

    obstacles.add((r_p, c_p))
    return squares


def solve3(n: int, piece: str, r_p: int, c_p: int, obstacles: set):
    """ Traverse pieces' paths and check for nearest obstacle
    using membership tests on a set. """

    # (x, y)
    hor_vert = ((0, 1), (1, 0), (0, -1), (-1, 0))  # Up, right, down, left
    diag = ((1, 1), (-1, -1), (1, -1), (-1, 1))
    moves = {'q': hor_vert + diag, 'b': diag, 'r': hor_vert}

    squares = 0
    for x, y in moves[piece]:
        r, c = r_p + y, c_p + x
        min_x = n - c_p if x > 0 else c_p - 1
        min_y = n - r_p if y > 0 else r_p - 1

        while 0 < r <= n and 0 < c <= n:
            if (r, c) in obstacles:
                if x: min_x = min(min_x, (c - c_p)*x - 1)
                if y: min_y = min(min_y, (r - r_p)*y - 1)
            r += y
            c += x

        squares += (min(min_x, min_y) if x and y
                    else min_x if x else min_y)

    return squares


def solve(n: int, pieces: list, positions: list, obstacles, method: int):
    # print(f"{method= }")
    method = (None, solve1, solve2, solve3)[method]

    squares_per_piece = {pos: (piece, method(n, piece, *pos, obstacles))
                            for piece, pos in zip(pieces, positions)}
    maxi = max(squares_per_piece.values(), key = lambda x: x[1])[1]

    return "{}\n{}".format(maxi,
                        '\n'.join(f"{details[0]} {' '.join(map(str, pos))}"
                                    for pos, details in squares_per_piece.items()
                                    if details[1] == maxi))


if __name__ == "__main__":
    n, p, k = map(int, input().split())
    pieces = input().split()
    positions = [tuple(map(int, input().split())) for _ in range(p)]
    if n == 1:
        print("0\n{} {}".format(pieces[0], ' '.join(map(str, positions[0]))))
        raise SystemExit

    if n <= 20 * 10**3:
        method = 1
        # Array should use <= ~400MB
        obstacles = bytearray(b'\1') * n**2
        for _ in range(k):
            r, c = map(int, input().split())
            obstacles[n*(r - 1) + c-1] = 0
        for r, c in positions:
            obstacles[n*(r - 1) + c-1] = 0
    elif k + p-1 < total_squares(n, pieces, positions):
        # Less obstacles than average number of squares on the pieces' paths
        method = 2
        obstacles = {tuple(map(int,input().split())) for _ in range(k)}
        obstacles.update(positions)
    else:
        method = 3
        obstacles = {tuple(map(int,input().split())) for _ in range(k)}
        obstacles.update(positions)


    print(solve(n, pieces, positions, obstacles, method))

