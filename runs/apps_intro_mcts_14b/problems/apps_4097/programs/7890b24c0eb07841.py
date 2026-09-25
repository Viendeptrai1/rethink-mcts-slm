import sys

def min_changes_to_arithmetic_progression(n, b):
    if n <= 2:
        return 0
    
    b.sort()
    
    def count_changes(diff):
        changes = 0
        for i in range(1, n):
            expected = b[0] + i * diff
            if abs(b[i] - expected) > 1:
                return float('inf')
            changes += abs(b[i] - expected)
        return changes // 2
    
    min_changes = float('inf')
    for d in range(-10**9, 10**9 + 1):
        if d == 0:
            continue
        min_changes = min(min_changes, count_changes(d))
    
    if min_changes == float('inf'):
        return -1
    return min_changes

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    b = list(map(int, data[1:n+1]))
    
    result = min_changes_to_arithmetic_progression(n, b)
    print(result)

if __name__ == "__main__":
    main()