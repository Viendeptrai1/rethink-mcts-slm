from collections import Counter
import sys

def find_valid_positions(n, m, p, a, b):
    valid_positions = []
    target_counter = Counter(b)
    
    for q in range(1, n - m * p + 2):
        current_counter = Counter(a[q-1:q+m*p-1:p])
        if current_counter == target_counter:
            valid_positions.append(q)
    
    return len(valid_positions), valid_positions

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    p = int(data[2])
    
    a = list(map(int, data[3:3+n]))
    b = list(map(int, data[3+n:3+n+m]))
    
    result_count, result_positions = find_valid_positions(n, m, p, a, b)
    
    print(result_count)
    print(" ".join(map(str, result_positions)))