import sys
from collections import Counter

def find_valid_positions(n, m, p, a, b):
    # Count occurrences of each element in b
    b_count = Counter(b)
    
    valid_positions = []
    
    # Iterate over all possible starting positions q
    for q in range(1, n - (m - 1) * p + 1):
        # Create a counter for the subsequence a[q], a[q] + p, ..., a[q] + (m - 1) * p
        subsequence_count = Counter(a[i] for i in range(q - 1, q + (m - 1) * p, p))
        
        # Check if the subsequence count matches the count of b
        if subsequence_count == b_count:
            valid_positions.append(q)
    
    return len(valid_positions), valid_positions

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    p = int(data[2])
    
    a = list(map(int, data[3:3 + n]))
    b = list(map(int, data[3 + n:]))
    
    result_count, result_positions = find_valid_positions(n, m, p, a, b)
    
    print(result_count)
    print(' '.join(map(str, result_positions)))

if __name__ == "__main__":
    main()