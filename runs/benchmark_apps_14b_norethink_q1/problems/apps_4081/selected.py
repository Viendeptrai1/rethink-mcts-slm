import sys
from typing import List

def solve():
    import sys
    import bisect
    
    def readints():
        return list(map(int, sys.stdin.read().split()))
    
    data = readints()
    n = data[0]
    a = data[1:]
    
    # Create a list of tuples (value, index)
    indexed_a = [(a[i], i) for i in range(n)]
    
    # Sort the list by value
    indexed_a.sort()
    
    # Extract the sorted values and their original indices
    sorted_values = [x[0] for x in indexed_a]
    sorted_indices = [x[1] for x in indexed_a]
    
    # Initialize the DP table
    dp = []
    path = []
    
    for i in range(n):
        val, idx = sorted_values[i], sorted_indices[i]
        
        # Find the position to replace in the DP table
        pos = bisect.bisect_left(dp, val)
        
        if pos == len(dp):
            dp.append(val)
            path.append('R' if idx < n - 1 - (len(dp) - 2) else 'L')
        else:
            dp[pos] = val
            path[pos] = 'R' if idx < n - 1 - pos else 'L'
    
    k = len(dp)
    result_path = ''.join(path[:k])
    
    print(k)
    print(result_path)

if __name__ == "__main__":
    solve()