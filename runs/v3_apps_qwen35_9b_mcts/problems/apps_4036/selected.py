import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    k = int(input_data[1])
    
    # Minimum possible sum: strictly increasing starting from 1
    # 1, 2, 3, ..., k -> sum = k*(k+1)/2
    min_sum = k * (k + 1) // 2
    
    # Maximum possible sum: doubling sequence
    # x, 2x, 4x, ..., x*2^(k-1) -> sum = x * (2^k - 1)
    # We need to find if there exists an x such that sum == n.
    # The maximum sum for a given starting x is when we double every time.
    # However, we can also think of it as: for a fixed starting x, the max sum is x * (2^k - 1).
    # But we need to check if n is within [min_sum, max_possible_sum].
    # What is the max possible sum? It's unbounded if x can be arbitrarily large?
    # No, because we need sum == n. So we are looking for a starting x.
    # The constraints on the sequence are: a[i+1] >= a[i] + 1 and a[i+1] <= 2*a[i].
    # To maximize the sum for a fixed starting x, we always choose a[i+1] = 2*a[i].
    # To minimize the sum for a fixed starting x, we always choose a[i+1] = a[i] + 1.
    
    # Let's define a function that given a starting value x, returns the minimum and maximum possible sums for a sequence of length k.
    # min_sum(x) = x + (x+1) + (x+2) + ... + (x+k-1) = k*x + k*(k-1)/2
    # max_sum(x) = x + 2x + 4x + ... + x*2^(k-1) = x * (2^k - 1)
    
    # We need to find an x such that min_sum(x) <= n <= max_sum(x).
    # Also, we need to construct the sequence.
    
    # First, check if n is small enough for the absolute minimum (starting at 1)
    if n < min_sum:
        print("NO")
        return
    
    # Calculate max possible sum starting from 1
    # If even starting from 1 and doubling every time, the sum is less than n, then it's impossible?
    # Wait, if we start with x=1, max sum is 2^k - 1.
    # If n > 2^k - 1, we might need a larger x.
    # But if we increase x, both min_sum and max_sum increase.
    # So we need to find x such that min_sum(x) <= n <= max_sum(x).
    
    # Let's find the range of valid x.
    # min_sum(x) = k*x + k*(k-1)/2 <= n
    # => k*x <= n - k*(k-1)/2
    # => x <= (n - k*(k-1)/2) / k
    # Let max_x_upper = (n - k*(k-1)//2) // k
    
    # max_sum(x) = x * (2^k - 1) >= n
    # => x >= n / (2^k - 1)
    # Let min_x_lower = ceil(n / (2^k - 1))
    
    # We need to find an integer x in [min_x_lower, max_x_upper].
    
    # Calculate powers of 2 carefully to avoid overflow issues (though Python handles large ints)
    # k up to 10^5, so 2^k is huge. But n is up to 10^9.
    # If 2^k - 1 > n, then min_x_lower = 1.
    # If 2^k - 1 is very large, then x must be 1.
    
    # Let's compute the threshold for 2^k - 1 vs n.
    # If k is large (e.g., k=30), 2^30 > 10^9.
    # So for k >= 30, 2^k - 1 > n, so min_x_lower = 1.
    
    if k >= 31:
        # 2^31 - 1 > 2*10^9 > n (since n <= 10^9)
        # So max_sum(1) > n. Thus min_x_lower = 1.
        min_x_lower = 1
    else:
        max_pow2 = 1 << k
        if max_pow2 - 1 >= n:
            min_x_lower = 1
        else:
            # x >= n / (2^k - 1)
            min_x_lower = (n + (max_pow2 - 1) - 1) // (max_pow2 - 1)
    
    # Calculate max_x_upper
    # k*x + k*(k-1)/2 <= n
    # k*x <= n - k*(k-1)/2
    term = k * (k - 1) // 2
    if n < term:
        # This case is already handled by n < min_sum check at the beginning
        # But just in case
        print("NO")
        return
    
    max_x_upper = (n - term) // k
    
    if min_x_lower > max_x_upper:
        print("NO")
        return
    
    # We have a valid range [min_x_lower, max_x_upper].
    # We need to pick an x in this range such that we can construct a sequence summing to n.
    # Actually, for any x in this range, is it guaranteed that we can form sum n?
    # Not necessarily. The set of achievable sums for a fixed x is a contiguous range [min_sum(x), max_sum(x)].
    # Why? Because we can adjust each step from min (x+1) to max (2x).
    # Specifically, let the sequence be a_1, a_2, ..., a_k.
    # a_1 = x.
    # a_2 can be any value in [x+1, 2x].
    # a_3 can be any value in [a_2+1, 2*a_2].
    # The set of possible sums is indeed contiguous because we can increment the sum by 1 by adjusting one of the later terms appropriately?
    # Let's verify.
    # Suppose we have a sequence. Can we increase the total sum by 1?
    # We can try to increase a_k. If a_k < 2*a_{k-1}, we can increase a_k by 1.
    # If a_k == 2*a_{k-1}, we might need to increase a_{k-1}.
    # Generally, yes, the range of sums is contiguous.
    # So if min_sum(x) <= n <= max_sum(x), then there exists a sequence starting with x summing to n.
    
    # So we just need to pick any x in [min_x_lower, max_x_upper].
    # Let's pick x = min_x_lower.
    x = min_x_lower
    
    # Now construct the sequence.
    # We start with a_1 = x.
    # We need to determine a_2, ..., a_k such that sum is n.
    # Strategy: Greedily make the sequence as small as possible (a[i+1] = a[i] + 1) until the last element,
    # or distribute the remaining sum.
    # Actually, a better strategy:
    # Start with the minimal sequence: x, x+1, x+2, ..., x+k-1.
    # Current sum = min_sum(x).
    # Remaining sum to add = n - min_sum(x).
    # We can add this remainder to the elements from right to left (a_k, a_{k-1}, ...),
    # respecting the constraint a[i] <= 2*a[i-1].
    # When we increase a[i], we might need to increase a[i-1] to satisfy a[i] <= 2*a[i-1]?
    # No, the constraint is a[i] <= 2*a[i-1]. If we increase a[i], we might violate this if a[i-1] is too small.
    # But we are building from left to right or right to left?
    # Let's build from left to right.
    # a_1 = x.
    # For i from 1 to k-1:
    #   We need to choose a_{i+1} in [a_i + 1, 2*a_i].
    #   We want to leave enough room for the remaining elements to sum up to the target.
    #   Let rem be the remaining sum needed after choosing a_{i+1}.
    #   The minimum sum for the remaining k - (i+1) elements starting with a_{i+1} is:
    #   min_rem = (k - i - 1) * a_{i+1} + (k - i - 1)*(k - i - 2)//2
    #   We need rem >= min_rem.
    #   Also, we need to be able to reach the max possible sum? No, we just need to hit exactly n.
    #   Since the range of sums is contiguous, we just need to ensure that the current choice allows us to reach the target.
    #   Actually, simpler approach:
    #   Start with the minimal sequence: a[i] = x + i.
    #   Calculate current sum S.
    #   Diff = n - S.
    #   We need to distribute Diff among the elements a_2, ..., a_k such that constraints are maintained.
    #   We can increase a_k as much as possible (up to 2*a_{k-1}), then a_{k-1}, etc.
    #   But increasing a_k might require increasing a_{k-1} if a_k was already at 2*a_{k-1}?
    #   No, if we increase a_{k-1}, the upper bound for a_k increases.
    #   So we can propagate the increase from right to left.
    #   Algorithm:
    #   1. Initialize a[i] = x + i for i=0..k-1 (0-indexed).
    #   2. Calculate current sum.
    #   3. diff = n - current_sum.
    #   4. Iterate from i = k-1 down to 1:
    #      We can increase a[i] by at most (2*a[i-1] - a[i]).
    #      But wait, if we increase a[i], we might need to increase a[i-1] later?
    #      No, we are going backwards. a[i-1] is already fixed (or will be fixed in the next step).
    #      Actually, if we increase a[i], the constraint a[i] <= 2*a[i-1] must hold.
    #      If we increase a[i], we don't affect the lower bound for a[i+1] (which is a[i]+1).
    #      But we do affect the upper bound for a[i+1].
    #      However, we are distributing the extra sum.
    #      Let's try to add as much as possible to a[i] without violating a[i] <= 2*a[i-1].
    #      But we also need to ensure that we can still form the rest of the sequence?
    #      Actually, since we start with the minimal sequence, any increase we make is valid as long as we don't exceed the doubling constraint.
    #      And since we are going backwards, when we are at i, a[i-1] is already "finalized" (we decided its value in the previous step of the loop? No, we go k-1 down to 1).
    #      Wait, if we go backwards:
    #      i = k-1: a[k-1] can be increased up to 2*a[k-2].
    #      i = k-2: a[k-2] can be increased up to 2*a[k-3].
    #      But if we increase a[k-2], the upper bound for a[k-1] increases.
    #      So we should process from right to left, but we need to be careful.
    #      Actually, the standard greedy approach for this problem is:
    #      Start with minimal sequence.
    #      diff = n - sum.
    #      For i from k-1 down to 1:
    #          max_add = 2 * a[i-1] - a[i]
    #          add = min(diff, max_add)
    #          a[i] += add
    #          diff -= add
    #      If diff > 0 after the loop, it means we couldn't distribute the sum.
    #      But wait, is it possible that diff > 0?
    #      We chose x such that max_sum(x) >= n.
    #      max_sum(x) is achieved when a[i] = 2*a[i-1] for all i.
    #      Our greedy strategy tries to push values to the right as much as possible.
    #      Does this achieve the maximum sum?
    #      Yes, because to maximize the sum, we want larger numbers at the end.
    #      By pushing as much as possible to a[k-1], then a[k-2], etc., we are effectively building the sequence towards the doubling sequence.
    #      So if n <= max_sum(x), diff should become 0.
    
    a = [0] * k
    for i in range(k):
        a[i] = x + i
    
    current_sum = sum(a)
    diff = n - current_sum
    
    # Distribute diff from right to left
    for i in range(k - 1, 0, -1):
        if diff <= 0:
            break
        # Maximum we can add to a[i] is limited by 2*a[i-1]
        limit = 2 * a[i-1] - a[i]
        add = min(diff, limit)
        a[i] += add
        diff -= add
    
    if diff > 0:
        # This should not happen if our bounds are correct
        print("NO")
        return
    
    # Verify the sum
    if sum(a) != n:
        print("NO")
        return
    
    # Verify constraints
    for i in range(k - 1):
        if a[i] < 1:
            print("NO")
            return
        if a[i+1] < a[i] + 1 or a[i+1] > 2 * a[i]:
            print("NO")
            return
    
    print("YES")
    print(*(a))

if __name__ == '__main__':
    solve()