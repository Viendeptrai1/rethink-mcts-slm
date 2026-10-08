import sys
from itertools import combinations

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    m = int(data[index + 1])
    index += 2
    
    a = list(map(int, data[index:index + n]))
    index += n
    
    segments = []
    for _ in range(m):
        l = int(data[index]) - 1
        r = int(data[index + 1]) - 1
        segments.append((l, r))
        index += 2
    
    max_diff = 0
    best_mask = 0
    best_segments = []
    
    for mask in range(1 << m):
        b = a[:]
        for j in range(m):
            if mask & (1 << j):
                l, r = segments[j]
                for i in range(l, r + 1):
                    b[i] -= 1
        
        current_max = max(b)
        current_min = min(b)
        current_diff = current_max - current_min
        
        if current_diff > max_diff:
            max_diff = current_diff
            best_mask = mask
            best_segments = [j + 1 for j in range(m) if mask & (1 << j)]
    
    print(max_diff)
    print(len(best_segments))
    print(*best_segments)

if __name__ == "__main__":
    main()