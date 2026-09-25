import sys

def min_changes_to_arithmetic_progression(n, b):
    if n <= 2:
        return 0
    
    def count_changes(diff):
        changes = 0
        for i in range(1, n):
            expected = b[i - 1] + diff
            if b[i] != expected:
                changes += abs(b[i] - expected)
                if changes > n // 2:
                    return float('inf')
        return changes
    
    min_changes = float('inf')
    
    for i in range(n):
        for j in range(i + 1, n):
            if j == i + 1:
                diff = 0
            else:
                diff = (b[j] - b[i]) // (j - i)
            
            if (b[j] - b[i]) % (j - i) == 0:
                changes = count_changes(diff)
                min_changes = min(min_changes, changes)
    
    if min_changes == float('inf'):
        return -1
    else:
        return min_changes

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    b = list(map(int, data[1:]))
    
    result = min_changes_to_arithmetic_progression(n, b)
    print(result)

if __name__ == "__main__":
    main()