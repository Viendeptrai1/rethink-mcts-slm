import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    n = int(next(iterator))
    m = int(next(iterator))
    
    a = []
    for _ in range(n):
        a.append(int(next(iterator)))
    
    subarray_sums = []
    for _ in range(m):
        l = int(next(iterator))
        r = int(next(iterator))
        # Convert 1-based indexing to 0-based
        current_sum = sum(a[l-1:r])
        subarray_sums.append(current_sum)
    
    # The total happiness is the sum of the sums of the chosen subarrays.
    # To maximize this, we simply choose all subarrays with a positive sum.
    max_happiness = sum(x for x in subarray_sums if x > 0)
    
    print(max_happiness)

if __name__ == "__main__":
    solve()