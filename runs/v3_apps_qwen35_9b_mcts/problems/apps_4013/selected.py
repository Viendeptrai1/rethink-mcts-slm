import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = []
    for i in range(n):
        a.append(int(data[i + 1]))
    
    a.sort()
    
    # Option 1: Remove the smallest element (first element after sort)
    # The new min is a[1], max is a[n-1]
    instability1 = a[n - 1] - a[1]
    
    # Option 2: Remove the largest element (last element after sort)
    # The new min is a[0], max is a[n-2]
    instability2 = a[n - 2] - a[0]
    
    print(min(instability1, instability2))

if __name__ == "__main__":
    solve()