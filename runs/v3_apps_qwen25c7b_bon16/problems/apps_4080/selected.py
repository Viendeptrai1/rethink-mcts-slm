def solve():
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
    
    # Sort segments by their starting point
    segments.sort(key=lambda x: x[0])
    
    # Greedy approach to maximize the difference
    applied_segments = []
    current_min = min(a)
    current_max = max(a)
    
    for i, (l, r) in enumerate(segments):
        new_min = current_min
        new_max = current_max
        
        if a[l] > current_min:
            new_min = current_min
        else:
            new_min = a[l]
        
        if a[r] < current_max:
            new_max = current_max
        else:
            new_max = a[r]
        
        if new_max - new_min > current_max - current_min:
            applied_segments.append(i + 1)
            current_min = new_min
            current_max = new_max
    
    max_diff = current_max - current_min
    
    print(max_diff)
    print(len(applied_segments))
    print(" ".join(map(str, applied_segments)))

if __name__ == "__main__":
    solve()