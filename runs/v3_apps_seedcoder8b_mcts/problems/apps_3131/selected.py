def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    a = list(map(int, data[2:2+N]))
    
    MOD = 1000000007
    
    # Sort the key values in descending order
    a.sort(reverse=True)
    
    # Sum the top K values
    result = sum(a[:K]) % MOD
    
    # Print the result
    print(result)