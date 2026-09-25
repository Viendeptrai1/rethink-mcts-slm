import sys
from collections import defaultdict

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    p = list(map(int, data[2:]))
    
    # Initialize variables
    balance = 0
    count = 0
    prefix_count = defaultdict(int)
    prefix_count[0] = 1
    
    for i in range(n):
        if p[i] < m:
            balance -= 1
        elif p[i] > m:
            balance += 1
        
        # We need the number of times we have seen this balance before
        # because it means there was a subarray ending at i with median m
        count += prefix_count[balance]
        count += prefix_count[balance - 1]
        
        # Update the prefix count
        prefix_count[balance] += 1
    
    print(count)

if __name__ == "__main__":
    main()