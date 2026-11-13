from typing import List

def max_calm_group_sum(n: int, a: List[int], b: List[int]) -> int:
    max_sum = 0
    for i in range(1 << n):
        group = [j for j in range(n) if i & (1 << j)]
        if len(group) >= 2:
            skills = [b[j] for j in group]
            calm = True
            for x in group:
                for y in group:
                    if x != y and all(a[x] & (1 << j) == a[y] & (1 << j) for j in range(60)):
                        calm = False
                        break
                if not calm:
                    break
            if calm:
                max_sum = max(max_sum, sum(skills))
    return max_sum

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:n+1]))
    b = list(map(int, data[n+1:2*n+1]))
    
    result = max_calm_group_sum(n, a, b)
    print(result)