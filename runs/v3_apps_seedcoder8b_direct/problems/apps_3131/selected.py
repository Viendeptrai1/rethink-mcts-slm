def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    MOD = 1000000007
    
    N = int(data[0])
    K = int(data[1])
    a = list(map(int, data[2:2+N]))
    
    # Sort the values of the keys in descending order
    a.sort(reverse=True)
    
    # Calculate the sum of the top K values
    result = sum(a[:K]) % MOD
    
    # Print the result
    print(result)