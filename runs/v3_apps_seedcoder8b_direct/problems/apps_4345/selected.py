def find_initial_sequences():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:n+1]))
    
    # Function to check if a sequence is strictly increasing
    def is_strictly_increasing(seq):
        return all(x < y for x, y in zip(seq, seq[1:]))
    
    # Function to check if a sequence is strictly decreasing
    def is_strictly_decreasing(seq):
        return all(x > y for x, y in zip(seq, seq[1:]))
    
    # Try to find the split point
    increasing = []
    decreasing = []
    res = [0] * n
    
    # Start with the first element
    increasing.append(a[0])
    res[0] = 0
    
    for i in range(1, n):
        if a[i] > increasing[-1]:
            increasing.append(a[i])
            res[i] = 0
        else:
            decreasing.append(a[i])
            res[i] = 1
    
    # Check if the found increasing and decreasing sequences are valid
    if is_strictly_increasing(increasing) and is_strictly_decreasing(decreasing):
        print("YES")
        print(" ".join(map(str, res)))
    else:
        print("NO")