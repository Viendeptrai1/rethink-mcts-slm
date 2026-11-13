import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    d = list(map(int, data[1:]))
    
    d.sort()
    
    # We need exactly n/2 problems in ABCs (difficulty < K)
    # and n/2 problems in ARCs (difficulty >= K).
    # Since the array is sorted:
    # The first n/2 elements must be < K.
    # The last n/2 elements must be >= K.
    
    half = n // 2
    
    # The largest element in the ABC group is d[half-1]
    # The smallest element in the ARC group is d[half]
    # For a valid K, we need: d[half-1] < K <= d[half]
    
    lower_bound = d[half - 1]
    upper_bound = d[half]
    
    # The number of integers K such that lower_bound < K <= upper_bound
    # is max(0, upper_bound - lower_bound)
    
    ans = max(0, upper_bound - lower_bound)
    print(ans)

if __name__ == "__main__":
    solve()