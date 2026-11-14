import sys
import math

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
    
    # Check if there is already a 1 in the array
    if 1 in a:
        # Count non-1 elements
        count_non_one = sum(1 for x in a if x != 1)
        print(count_non_one)
        return
    
    # If no 1 exists, we need to find the shortest contiguous subarray with GCD = 1
    min_len = float('inf')
    
    # We can optimize this by checking all subarrays starting at each index i
    # and extending until GCD becomes 1 or we reach the end.
    # Since n <= 2000, O(n^2) is acceptable.
    
    for i in range(n):
        current_gcd = a[i]
        for j in range(i, n):
            current_gcd = gcd(current_gcd, a[j])
            if current_gcd == 1:
                length = j - i + 1
                if length < min_len:
                    min_len = length
                break # No need to extend further for this start index, GCD will only decrease or stay 1
    
    if min_len == float('inf'):
        print(-1)
    else:
        # Operations needed:
        # 1. (min_len - 1) operations to create one '1' from the subarray of length min_len
        # 2. (n - 1) operations to propagate this '1' to the remaining (n-1) elements
        # Total = (min_len - 1) + (n - 1)
        print(min_len - 1 + n - 1)

if __name__ == "__main__":
    solve()