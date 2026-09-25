import sys

def min_changes_to_arithmetic_progression(n, b):
    if n <= 2:
        return 0

    def calculate_changes(diff):
        changes = 0
        for i in range(1, n):
            expected = b[i - 1] + diff
            if b[i] != expected:
                if abs(b[i] - expected) == 1:
                    changes += 1
                else:
                    return float('inf')
        return changes

    min_changes = float('inf')
    for d in range(-1, 2):
        min_changes = min(min_changes, calculate_changes(d))

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