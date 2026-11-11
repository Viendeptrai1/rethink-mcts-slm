import sys

def count_returnable_rooms(t, test_cases):
    results = []
    for n, s in test_cases:
        # Initialize arrays to keep track of reachable rooms in both directions
        forward_reachable = [False] * n
        backward_reachable = [False] * n
        
        # Mark all rooms as reachable from themselves
        for i in range(n):
            forward_reachable[i] = True
            backward_reachable[i] = True
        
        # Check forward reachability
        for i in range(n):
            if s[i] == '>' or s[i] == '-':
                forward_reachable[(i + 1) % n] |= forward_reachable[i]
        
        # Check backward reachability
        for i in range(n - 1, -1, -1):
            if s[i] == '<' or s[i] == '-':
                backward_reachable[(i - 1) % n] |= backward_reachable[i]
        
        # Count rooms that are reachable in both directions
        returnable_count = sum(1 for i in range(n) if forward_reachable[i] and backward_reachable[i])
        results.append(returnable_count)
    
    return results

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    index = 1
    test_cases = []
    
    for _ in range(t):
        n = int(data[index])
        s = data[index + 1]
        test_cases.append((n, s))
        index += 2
    
    results = count_returnable_rooms(t, test_cases)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()