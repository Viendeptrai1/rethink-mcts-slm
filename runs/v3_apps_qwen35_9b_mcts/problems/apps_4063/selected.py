import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    d = []
    for i in range(n):
        d.append(int(data[i+1]))
    
    d.sort()
    
    # The first N/2 problems will be ABCs (difficulty < K)
    # The last N/2 problems will be ARCs (difficulty >= K)
    # We need K such that:
    # d[N/2 - 1] < K <= d[N/2]
    
    lower_bound = d[n // 2 - 1]
    upper_bound = d[n // 2]
    
    # The number of integers K satisfying lower_bound < K <= upper_bound
    # is max(0, upper_bound - lower_bound)
    
    ans = max(0, upper_bound - lower_bound)
    print(ans)

if __name__ == "__main__":
    solve()