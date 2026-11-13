import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    a = [int(x) for x in input_data[1:]]
    
    a.sort()
    
    # Option 1: Remove the smallest element (index 0)
    # The new min is a[1], max is a[n-1]
    ans = a[n-1] - a[1]
    
    # Option 2: Remove the largest element (index n-1)
    # The new min is a[0], max is a[n-2]
    ans = min(ans, a[n-2] - a[0])
    
    print(ans)

if __name__ == "__main__":
    solve()