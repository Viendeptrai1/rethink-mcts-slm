import sys
from typing import List

def solve() -> int:
    input_data = sys.stdin.read().split()
    if not input_data:
        return 0
    
    n = int(input_data[0])
    X = int(input_data[1])
    prices = [int(x) for x in input_data[2:2+n]]
    
    # Sort prices to easily find the largest and second largest
    prices.sort()
    
    # We want to select a subset S of items such that for any two items a, b in S:
    # a + b <= X
    # We want to maximize |S|.
    
    # Strategy:
    # If we select k items, let them be sorted as s_1 <= s_2 <= ... <= s_k.
    # The condition "for any pair, sum <= X" is equivalent to "the two largest sum <= X".
    # That is, s_{k-1} + s_k <= X.
    # To maximize k, we should pick the smallest k items from the sorted array.
    # Why? Because picking smaller items makes it easier to satisfy the sum constraint.
    # If the smallest k items satisfy the condition (prices[n-k-1] + prices[n-k] <= X),
    # then any other set of k items will also satisfy it (since they would be >= these).
    # However, we might be able to pick MORE than k items if we don't pick the absolute smallest,
    # but actually, to maximize the count, picking the smallest available items is always optimal.
    # Let's verify:
    # Suppose the optimal set has size M. Let its elements be p_1 <= p_2 <= ... <= p_M.
    # Condition: p_{M-1} + p_M <= X.
    # Consider the M smallest items in the entire array: q_1 <= q_2 <= ... <= q_M.
    # Since q_i <= p_i for all i, we have q_{M-1} + q_M <= p_{M-1} + p_M <= X.
    # So if a set of size M exists, the M smallest items also form a valid set.
    # Therefore, we just need to find the largest M such that the sum of the two largest
    # among the M smallest items is <= X.
    
    # Let's iterate M from n down to 0? Or simpler:
    # Check the largest possible M.
    # The M smallest items are prices[0], ..., prices[M-1].
    # The two largest are prices[M-2] and prices[M-1].
    # We need prices[M-2] + prices[M-1] <= X.
    
    # Edge case: if M=0 or M=1, the condition is vacuously true (no pair exists).
    # So we can always mark at least min(n, 1) items? Actually if n >= 1, answer is at least 1.
    # If n=0, answer 0.
    
    if n == 0:
        return 0
    
    # If we pick 1 item, no pair exists, so condition holds. Max possible is at least 1.
    # We need to find max M in [1, n] such that prices[M-2] + prices[M-1] <= X.
    # Note: for M=1, there is no M-2 index. So M=1 is always valid.
    
    # We can iterate M from n down to 1 and find the first one that works.
    # Since the condition prices[M-2] + prices[M-1] <= X is monotonic?
    # As M increases, prices[M-1] increases (or stays same), so the sum increases.
    # Thus, if it holds for M, it holds for all M' < M (provided M' >= 2).
    # So we can use binary search or just linear scan from n downwards.
    # Given n <= 10^5, linear scan is fine.
    
    # Check from largest possible M downwards
    # Special handling for M=1 (always valid) and M=0 (valid but we want max).
    
    ans = 1  # At least 1 item is always possible
    
    # Check M from n down to 2
    for m in range(n, 1, -1):
        # The two largest in the set of m smallest items are at indices m-2 and m-1
        if prices[m-2] + prices[m-1] <= X:
            ans = m
            break
            
    return ans

if __name__ == "__main__":
    print(solve())