def solve_bands():
    S = int(input())
    x1, y1 = map(int, input().split())
    seq1 = input().strip()
    x2, y2 = map(int, input().split())
    seq2 = input().strip()

    moves = {'u': (-1, 0), 'd': (1, 0), 'l': (0, -1), 'r': (0, 1)}

    def trace_path(x, y, seq):
        path_time = {}
        step = 0
        path_time[(x, y)] = step
        for move in seq:
            dx, dy = moves[move]
            x += dx
            y += dy
            step += 1
            if 0 <= x < S and 0 <= y < S:
                if (x, y) not in path_time:
                    path_time[(x, y)] = step
        return path_time

    path1 = trace_path(x1, y1, seq1)
    path2 = trace_path(x2, y2, seq2)

    overlaps = set(path1.keys()) & set(path2.keys())
    if not overlaps:
        print(0)
        return

    band1_first = band2_first = 0
    for pos in overlaps:
        t1 = path1[pos]
        t2 = path2[pos]
        if t1 < t2:
            band1_first += 1
        elif t2 < t1:
            band2_first += 1

    if band1_first > 0 and band2_first > 0:
        print("Impossible")
    else:
        print(len(overlaps))

solve_bands()
