import sys
from collections import defaultdict

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    H = int(data[0])
    W = int(data[1])
    M = int(data[2])
    
    targets = []
    for i in range(M):
        h = int(data[3 + 2 * i])
        w = int(data[4 + 2 * i])
        targets.append((h, w))
    
    row_count = defaultdict(int)
    col_count = defaultdict(int)
    
    for h, w in targets:
        row_count[h] += 1
        col_count[w] += 1
    
    max_row = max(row_count.values())
    max_col = max(col_count.values())
    
    max_targets_destroyed = max_row + max_col
    
    if max_row == max_col:
        # Check if there is any intersection point (h, w) such that both row h and column w have max targets
        intersection_count = 0
        for h, w in targets:
            if row_count[h] == max_row and col_count[w] == max_col:
                intersection_count += 1
        
        if intersection_count > 0:
            max_targets_destroyed -= 1
    
    print(max_targets_destroyed)

if __name__ == "__main__":
    main()