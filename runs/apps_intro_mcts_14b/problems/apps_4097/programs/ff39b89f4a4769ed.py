import sys

def min_changes_to_arithmetic_progression(n, b):
    if n <= 2:
        return 0
    
    b.sort()
    min_changes = float('inf')
    
    # Try all possible common differences
    for d in range(-10**9, 10**9 + 1):
        changes = 0
        valid = True
        for i in range(1, n):
            expected = b[0] + i * d
            if abs(b[i] - expected) > 1:
                valid = False
                break
            changes += abs(b[i] - expected)
        if valid:
            min_changes = min(min_changes, changes)
    
    return min_changes if min_changes != float('inf') else -1

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