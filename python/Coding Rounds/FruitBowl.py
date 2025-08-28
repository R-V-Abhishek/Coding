import math
import sys

def calculate_fruit_bowl_perimeter():
    def distance(p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def cross_product(p1, p2, p3):
        return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

    data = sys.stdin.read().strip().split()
    if not data:
        return
    nums = list(map(int, data))

    def solve_case(points):
        if not points:
            return 0
        pts = sorted(points)
        lower = []
        for p in pts:
            while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(p)
        per = 0.0
        for i in range(len(lower) - 1):
            per += distance(lower[i], lower[i + 1])
        def round_half_up_positive(x: float, eps: float = 1e-9) -> int:
            f = math.floor(x)
            return f + 1 if (x - f + eps) >= 0.5 else f
        return round_half_up_positive(per)

    out_lines = []
    total = len(nums)
    # Detect single test vs multiple tests by token count pattern
    if total >= 1:
        first = nums[0]
        # Single test if exactly 1 + 2*n tokens
        if 1 + 2 * first == total:
            n = first
            pts = []
            i = 1
            for _ in range(n):
                x = nums[i]; y = nums[i + 1]
                i += 2
                pts.append((x, y))
            out_lines.append(str(solve_case(pts)))
        else:
            t = first
            i = 1
            for _ in range(t):
                if i >= total:
                    break
                n = nums[i]; i += 1
                pts = []
                for _ in range(n):
                    if i + 1 >= total:
                        break
                    x = nums[i]; y = nums[i + 1]
                    i += 2
                    pts.append((x, y))
                out_lines.append(str(solve_case(pts)))
    if out_lines:
        sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    calculate_fruit_bowl_perimeter()
