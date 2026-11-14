import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    a = int(input_data[0])
    s = input_data[1]
    n = len(s)
    
    # Convert string to list of integers
    digits = [int(c) for c in s]
    
    # Precompute all subarray sums
    # Since n <= 4000, O(n^2) is acceptable (16 million operations)
    sub_sums = []
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += digits[j]
            sub_sums.append(current_sum)
    
    # Count frequency of each subarray sum
    from collections import Counter
    freq = Counter(sub_sums)
    
    count = 0
    
    if a == 0:
        # Special case: product is 0
        # We need sum1 * sum2 = 0, so at least one sum is 0
        # Count pairs (i, j) where sub_sums[i] * sub_sums[j] == 0
        # This happens if sub_sums[i] == 0 OR sub_sums[j] == 0
        # Total pairs = (total_subarrays)^2 - (non_zero_pairs)
        # Or more directly: count pairs where at least one is 0
        # Let Z be count of zeros, T be total number of subarrays
        # Pairs with at least one zero = Z*T - Z*Z + Z*Z? No.
        # Pairs (x, y) where x* y = 0:
        # If x=0, y can be anything: Z * T
        # If y=0, x can be anything: T * Z
        # But we double counted (0,0): Z * Z
        # So total = Z*T + T*Z - Z*Z = 2*Z*T - Z*Z
        # Wait, let's re-derive:
        # We are choosing two subarrays independently.
        # Let S be the set of all subarray sums.
        # We want number of pairs (u, v) in S x S such that u*v = 0.
        # This is equivalent to: u=0 OR v=0.
        # By inclusion-exclusion: |{u=0}|*|S| + |S|*|{v=0}| - |{u=0}|*|{v=0}|
        # = Z*T + T*Z - Z*Z = 2*Z*T - Z*Z
        # Where T = len(sub_sums) = n*(n+1)//2
        Z = freq[0]
        T = len(sub_sums)
        count = 2 * Z * T - Z * Z
    else:
        # General case: a > 0
        # We need sum1 * sum2 = a
        # Iterate over all possible values of sum1 that are divisors of a
        # Or simply iterate over all unique sums present in our data
        # Since the number of unique sums can be up to O(n^2), we iterate over the freq dict
        
        # To optimize, we only check divisors of a
        # But a can be up to 10^9, so finding divisors is fast enough.
        # However, iterating over freq keys is also O(n^2) in worst case, which is fine.
        # Let's iterate over the keys of freq.
        
        for val1, count1 in freq.items():
            if val1 == 0:
                continue
            if a % val1 == 0:
                val2 = a // val1
                if val2 in freq:
                    count2 = freq[val2]
                    if val1 == val2:
                        # If val1 == val2, we are choosing two subarrays with same sum
                        # Number of ways = count1 * count1
                        count += count1 * count1
                    else:
                        # val1 != val2
                        # Number of ways = count1 * count2
                        count += count1 * count2
    
    print(count)

if __name__ == '__main__':
    solve()