import sys

def min_changes_to_arithmetic_progression(n, b):
    if n <= 2:
        return 0
    
    changes = []
    
    # Calculate potential differences
    d1 = b[1] - b[0]
    d2 = b[n-1] - b[n-2]
    
    # Check if we can form an arithmetic progression with d1
    changes_d1 = 0
    for i in range(1, n):
        expected = b[0] + i * d1
        if abs(b[i] - expected) > 1:
            changes_d1 = -1
            break
        elif b[i] != expected:
            changes_d1 += 1
    
    # Check if we can form an arithmetic progression with d2
    changes_d2 = 0
    for i in range(n-2, -1, -1):
        expected = b[n-1] - (n-1-i) * d2
        if abs(b[i] - expected) > 1:
            changes_d2 = -1
            break
        elif b[i] != expected:
            changes_d2 += 1
    
    # If both d1 and d2 are valid, choose the minimum
    if changes_d1 >= 0 and changes_d2 >= 0:
        return min(changes_d1, changes_d2)
    elif changes_d1 >= 0:
        return changes_d1
    elif changes_d2 >= 0:
        return changes_d2
    else:
        return -1

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