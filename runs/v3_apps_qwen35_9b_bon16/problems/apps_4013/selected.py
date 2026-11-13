import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = [int(data[i + 1]) for i in range(n)]
    
    a.sort()
    
    min_instability = float('inf')
    
    # Option 1: Remove the smallest element
    # The new min is a[1], max is a[n-1]
    inst1 = a[n - 1] - a[1]
    min_instability = min(min_instability, inst1)
    
    # Option 2: Remove the largest element
    # The new min is a[0], max is a[n-2]
    inst2 = a[n - 2] - a[0]
    min_instability = min(min_instability, inst2)
    
    print(min_instability)

if __name__ == "__main__":
    solve()