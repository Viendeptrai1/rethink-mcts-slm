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
    a = list(map(int, input_data[1:1+n]))
    
    # Count existing 1s
    count_ones = 0
    for x in a:
        if x == 1:
            count_ones += 1
    
    if count_ones > 0:
        # If there is at least one 1, we just need to spread it to others.
        # Each non-1 element needs 1 operation to become 1 if adjacent to a 1.
        # So answer is (n - count_ones).
        print(n - count_ones)
        return
    
    # No 1s initially. We need to create a 1 first.
    # We look for the shortest subarray a[i..j] such that gcd of all elements in it is 1.
    # If no such subarray exists, it's impossible.
    
    min_len = float('inf')
    
    # Since n <= 2000, O(n^2) is acceptable.
    for i in range(n):
        current_gcd = a[i]
        for j in range(i, n):
            current_gcd = gcd(current_gcd, a[j])
            if current_gcd == 1:
                # Length of subarray is j - i + 1
                length = j - i + 1
                if length < min_len:
                    min_len = length
                # Since gcd can only decrease or stay same, once it becomes 1, 
                # any extension will also have gcd 1, but we want minimum length.
                # So we can break early for this i? 
                # Actually, extending the subarray increases length, so the first time we hit 1 is the minimal for this i.
                break
    
    if min_len == float('inf'):
        print(-1)
    else:
        # To create one 1, we need (min_len - 1) operations on the subarray of size min_len.
        # After creating one 1, we need (n - 1) operations to turn the rest into 1s.
        # Total = (min_len - 1) + (n - 1)
        print(min_len - 1 + n - 1)

if __name__ == "__main__":
    solve()