import sys
from collections import Counter

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    H = int(data[0])
    W = int(data[1])
    M = int(data[2])
    
    h_positions = [int(data[3 + 2 * i]) for i in range(M)]
    w_positions = [int(data[4 + 2 * i]) for i in range(M)]
    
    row_counter = Counter(h_positions)
    col_counter = Counter(w_positions)
    
    max_row_count = max(row_counter.values())
    max_col_count = max(col_counter.values())
    
    max_targets_destroyed = max_row_count + max_col_count
    
    # Check if there is any intersection point that has been counted twice
    intersection_count = 0
    for h in row_counter:
        if row_counter[h] == max_row_count:
            for w in col_counter:
                if col_counter[w] == max_col_count:
                    if (h, w) in zip(h_positions, w_positions):
                        intersection_count += 1
                        break
    
    if intersection_count > 1:
        max_targets_destroyed -= 1
    
    print(max_targets_destroyed)

if __name__ == "__main__":
    main()