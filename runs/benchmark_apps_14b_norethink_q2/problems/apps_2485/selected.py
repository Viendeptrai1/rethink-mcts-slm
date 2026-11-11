import sys
from collections import defaultdict

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    H = int(data[0])
    W = int(data[1])
    M = int(data[2])
    
    row_count = defaultdict(int)
    col_count = defaultdict(int)
    
    for i in range(M):
        h = int(data[3 + 2 * i])
        w = int(data[4 + 2 * i])
        row_count[h] += 1
        col_count[w] += 1
    
    max_row = max(row_count.values())
    max_col = max(col_count.values())
    
    max_targets_destroyed = max_row + max_col
    
    # Check if there is any intersection where bomb can be placed to destroy more targets
    for i in range(M):
        h = int(data[3 + 2 * i])
        w = int(data[4 + 2 * i])
        if row_count[h] == max_row and col_count[w] == max_col:
            max_targets_destroyed -= 1
            break
    
    print(max_targets_destroyed)

if __name__ == "__main__":
    main()