from typing import List

def can_hit_all_targets(N: int, targets: List[List[int]]) -> str:
    def slope(x1, y1, x2, y2):
        return float('inf') if x2 == x1 else (y2 - y1) / (x2 - x1)
    
    if N <= 2:
        return "success"
    
    slopes = set()
    for i in range(N):
        for j in range(i + 1, N):
            slopes.add(slope(targets[i][0], targets[i][1], targets[j][0], targets[j][1]))
    
    if len(slopes) > 2:
        return "failure"
    
    return "success"

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    N = int(data[0])
    targets = [list(map(int, data[i+1].split())) for i in range(N)]
    
    result = can_hit_all_targets(N, targets)
    print(result)