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
    best_segments = []
    
    for k in range(m + 1):
        for combo in combinations(range(m), k):
            b = a[:]
            for seg in combo:
                l, r = segments[seg]
                for i in range(l, r + 1):
                    b[i] -= 1
            
            current_max = max(b)
            current_min = min(b)
            current_diff = current_max - current_min
            
            if current_diff > max_diff:
                max_diff = current_diff
                best_segments = combo
    
    print(max_diff)
    print(len(best_segments))
    print(' '.join(map(str, [x + 1 for x in best_segments])))

if __name__ == "__main__":
    main()