import sys
import math

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(20000)

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    a = []
    for i in range(n):
        a.append(int(input_data[1 + i]))
    
    # Count existing 1s
    count_ones = 0
    for x in a:
        if x == 1:
            count_ones += 1
    
    if count_ones > 0:
        # If there is at least one 1, we just need to convert the rest.
        # Each non-1 element can be converted to 1 by operating with an adjacent 1.
        # Actually, if we have a 1 at index i, we can propagate it to neighbors.
        # To convert a segment of non-1s adjacent to a 1, each takes 1 operation.
        # Total operations = (n - count_ones).
        print(n - count_ones)
        return
    
    # If no 1s exist, we need to create a 1 first.
    # We look for the shortest subarray a[i..j] such that gcd(a[i], ..., a[j]) == 1.
    # Let the length of this subarray be L = j - i + 1.
    # The number of operations to create a 1 from this subarray is L - 1.
    # Once we have one 1, we need (n - 1) more operations to convert the rest.
    # Total = (L - 1) + (n - 1) = n + L - 2.
    # We need to minimize L.
    
    min_len = n + 1  # Initialize with a value larger than any possible valid length
    
    # We can optimize this. Since n <= 2000, O(n^2) is acceptable.
    # We iterate over all starting points i.
    # For each i, we expand j from i to n-1 and maintain the running gcd.
    # If running gcd becomes 1, we update min_len and break inner loop (since extending further won't reduce length).
    
    for i in range(n):
        current_gcd = a[i]
        for j in range(i, n):
            current_gcd = gcd(current_gcd, a[j])
            if current_gcd == 1:
                length = j - i + 1
                if length < min_len:
                    min_len = length
                break  # No need to extend further for this i, length will only increase
    
    if min_len > n:
        # Impossible to create a 1
        print(-1)
    else:
        # Operations to create one 1: min_len - 1
        # Operations to convert remaining n-1 elements: n - 1
        # Total: (min_len - 1) + (n - 1) = n + min_len - 2
        print(n + min_len - 2)

if __name__ == "__main__":
    solve()