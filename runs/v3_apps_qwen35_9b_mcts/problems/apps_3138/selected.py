import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    a = [int(x) for x in input_data[1:]]

    count = 0
    # Since product grows exponentially and sum linearly, valid ranges are very short.
    # Even with 1s, if we have k 1s and one number x > 1, sum = k + x, product = x.
    # k + x = x => k = 0, so no 1s allowed if there is a number > 1.
    # If all numbers are 1, sum = k, product = 1. k = 1 => length 1, but we need length >= 2.
    # So valid ranges must be short. We can safely check all subarrays of length up to 12.
    # Why 12? 2^12 = 4096. If we have twelve 2s, sum=24, product=4096.
    # If we have eleven 2s and one 1, sum=23, product=2048.
    # The gap widens rapidly. A length of 12 is more than sufficient to cover all cases.
    
    limit = 12
    
    for i in range(n):
        current_sum = 0
        current_prod = 1
        for j in range(i, min(i + limit, n)):
            val = a[j]
            current_sum += val
            current_prod *= val
            
            if j - i + 1 >= 2:
                if current_sum == current_prod:
                    count += 1
            
            # Optimization: if product already exceeds sum significantly and we are adding 1s,
            # it will never catch up. However, since our limit is small, we don't strictly need
            # this break, but it helps if we had a larger limit. Given the exponential growth,
            # once prod > sum + (remaining possible sum increase), we can stop.
            # But with limit=12, simple iteration is fast enough.
            
            # Early exit if product becomes too large relative to sum for the remaining elements
            # In the worst case of all 1s, product stays 1, sum increases.
            # If we have a number >= 2, product grows fast.
            # Let's add a check: if current_prod > current_sum + (limit - (j-i+1)) * 10^9, break?
            # Actually, max value is 10^9. If we have a 10^9, sum is at most 10^9 + 11*10^9 approx.
            # But product would be 10^9 * ... which is huge.
            # So if current_prod > current_sum + (limit - (j-i+1)) * 1000000000, we can break?
            # Actually, simpler: if current_prod > current_sum + (limit - (j-i+1)) * 10^9, break.
            # But since limit is small, let's just rely on the loop bound.
            # However, to be safe against overflow in languages with fixed integers (not Python),
            # Python handles large ints automatically. The only concern is time.
            # With N=200,000 and limit=12, operations ~ 2.4 million, which is well within time limits.
            
            # One edge case: if we have many 1s, product stays 1, sum increases.
            # If sum == 1 and length >= 2, impossible since numbers are positive integers (>=1).
            # If all are 1s: sum = L, prod = 1. L=1 => length 1 (invalid). So no solution for all 1s.
            # So we don't need to worry about the "all 1s" case producing false positives.
            
            # Let's add a break condition to be efficient:
            # If current_prod > current_sum + (limit - (j-i+1)) * 1000000000, then even if all remaining are 10^9,
            # sum won't catch up. But actually, if we have a huge number, product explodes.
            # If current_prod > current_sum + (limit - (j-i+1)) * 10^9, break.
            # This prevents unnecessary multiplications if numbers are huge.
            remaining_len = limit - (j - i + 1)
            if remaining_len > 0:
                max_possible_sum_increase = remaining_len * 1000000000
                if current_prod > current_sum + max_possible_sum_increase:
                    break

    print(count)

if __name__ == "__main__":
    solve()