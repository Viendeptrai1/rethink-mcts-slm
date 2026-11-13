from typing import List

def max_significance(n: int, m: int, d: int, physics_cups: List[List[int]], info_cups: List[List[int]]) -> int:
    def binary_search(cups: List[List[int]], target_width: int) -> int:
        left, right = 0, len(cups)
        while left < right:
            mid = (left + right) // 2
            if sum(cup[1] for cup in cups[:mid + 1]) > target_width:
                right = mid
            else:
                left = mid + 1
        return left

    physics_cups.sort(key=lambda x: (-x[0], -x[1]))
    info_cups.sort(key=lambda x: (-x[0], -x[1]))

    best_significance = 0
    for i in range(min(len(physics_cups), 1), min(len(physics_cups), n) + 1):
        for j in range(min(len(info_cups), 1), min(len(info_cups), m) + 1):
            total_width = sum(physics_cups[k][1] for k in range(i))
            total_width += sum(info_cups[l][1] for l in range(j))
            if total_width <= d:
                total_significance = sum(physics_cups[k][0] for k in range(i))
                total_significance += sum(info_cups[l][0] for l in range(j))
                if total_significance > best_significance:
                    best_significance = total_significance

    return best_significance

# Read input
n, m, d = map(int, input().split())
physics_cups = [list(map(int, input().split())) for _ in range(n)]
info_cups = [list(map(int, input().split())) for _ in range(m)]

# Calculate and print result
result = max_significance(n, m, d, physics_cups, info_cups)
print(result)