def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    m = int(data[index + 1])
    index += 2
    
    queries = []
    for _ in range(m):
        l = int(data[index]) - 1
        r = int(data[index + 1]) - 1
        index += 2
        queries.append((l, r))
    
    # Initialize the array with zeros
    a = [0] * n
    
    # Sort queries by length in descending order
    queries.sort(key=lambda x: x[1] - x[0], reverse=True)
    
    # Fill the array with values to maximize the minimum mex
    used = set()
    for l, r in queries:
        for i in range(l, r + 1):
            if len(used) == i - l:
                a[i] = len(used)
                used.add(a[i])
    
    # Calculate the mex for each query
    min_mex = float('inf')
    current_mex = 0
    current_set = set()
    for l, r in queries:
        for i in range(l, r + 1):
            if a[i] not in current_set:
                current_set.add(a[i])
            else:
                while current_mex in current_set:
                    current_mex += 1
                current_set.add(current_mex)
        
        if len(current_set) < min_mex:
            min_mex = len(current_set)
    
    print(min_mex)
    print(" ".join(map(str, a)))

solve()