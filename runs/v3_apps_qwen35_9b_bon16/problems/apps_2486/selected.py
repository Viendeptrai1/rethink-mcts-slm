import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    N = int(next(iterator))
    K = int(next(iterator))
    A = []
    for _ in range(N):
        A.append(int(next(iterator)))
    
    # Sort A to facilitate the calculation of the sum of the smallest m elements
    sorted_A = sorted(A)
    
    # Calculate prefix sums of the sorted array
    # prefix_sum[i] will be the sum of the first i elements (sorted_A[0] to sorted_A[i-1])
    prefix_sum = [0] * (N + 1)
    for i in range(N):
        prefix_sum[i+1] = prefix_sum[i] + sorted_A[i]
    
    # To determine if a card is unnecessary, we need to check if there exists a good subset containing it
    # such that removing it results in a subset that is NOT good.
    #
    # Consider a card with value 'x'.
    # A subset S containing 'x' is good if sum(S) >= K.
    # The subset S without 'x' is S' = S \ {x}.
    # The card is NOT unnecessary if there exists a good subset S containing 'x' such that sum(S') < K.
    # This is equivalent to: sum(S) >= K AND sum(S) - x < K.
    # Which simplifies to: K <= sum(S) < K + x.
    #
    # So, the card 'x' is NOT unnecessary if and only if there exists a subset of the OTHER cards (excluding 'x')
    # whose sum, say 's', satisfies: K - x <= s < K.
    #
    # If such a subset exists, then adding 'x' to it gives a sum s + x which is in [K, K + x - 1], so it's good.
    # But the original subset s is < K, so it's not good. Thus, removing 'x' breaks the goodness.
    #
    # Conversely, if no such subset exists for the other cards, then for any subset of other cards with sum s:
    #   - If s < K - x, then s + x < K, so adding 'x' doesn't make it good. (This subset doesn't matter)
    #   - If s >= K, then the subset itself is already good. We are looking for a good subset containing 'x'
    #     where removing 'x' makes it bad. If s >= K, then s is good. If we add 'x', sum is s+x >= K (still good).
    #     Removing 'x' leaves s, which is >= K, so it is still good.
    #     So we only care about subsets of others that are NOT good (s < K).
    #     Among those, we need one where s + x >= K.
    #     This means we need s >= K - x.
    #     So we need a subset of others with sum s in [K-x, K-1].
    #
    # Therefore, card 'x' is unnecessary if and only if the maximum possible sum of a subset of OTHER cards
    # that is strictly less than K is actually less than K - x.
    # In other words, if max_subset_sum_less_than_K(others) < K - x, then no such s exists, so card is unnecessary.
    # Otherwise (if max_subset_sum_less_than_K(others) >= K - x), then there exists such an s, so card is NOT unnecessary.
    #
    # Strategy:
    # 1. Consider all cards. We want to know for each card i, what is the maximum sum of a subset of {all cards} \ {i}
    #    that is < K.
    # 2. If we can efficiently calculate this for each i, we can determine the answer.
    #
    # Let's sort the array A.
    # For a fixed card i (with value A[i] in the sorted array, but we need to handle duplicates carefully by index),
    # the set of "other" cards is A without the element at that specific index.
    # However, since the condition depends only on the values, if there are duplicate values, removing one instance
    # is the same as removing another instance of the same value in terms of the set of available sums?
    # Not exactly. If we have two 1s, and we remove one, the other remains. If we remove the other, the first remains.
    # The set of achievable sums is the same because the multiset of remaining values is the same.
    # So we can process by value or by index, but since N is up to 5000, O(N^2) is acceptable (2.5 * 10^7 ops).
    #
    # O(N^2) approach:
    # For each card i:
    #   Consider the list of other cards.
    #   Find the maximum sum < K achievable using a subset of these other cards.
    #   Let this max sum be M_i.
    #   If M_i < K - A[i], then card i is unnecessary.
    #   Else, it is not unnecessary.
    #
    # How to find M_i efficiently for each i?
    # Since K <= 5000, we can use dynamic programming (knapsack-like).
    # dp[s] = true if sum s is achievable.
    # We need the largest s < K such that dp[s] is true.
    #
    # Algorithm:
    # 1. Sort A.
    # 2. Precompute something? Or just run O(N*K) for each i?
    #    Total complexity: O(N * (N + K)) = O(N^2 + N*K).
    #    With N=5000, K=5000, N*K = 2.5 * 10^7.
    #    N^2 = 2.5 * 10^7.
    #    Total ~ 5 * 10^7 operations. In Python, this might be tight but let's try to optimize.
    #    Actually, we can optimize the DP part.
    #
    # Optimization:
    # Instead of running full DP for each removal, notice that removing an element from the set of numbers
    # affects the reachable sums.
    # However, given the constraints and Python speed, a clean O(N*(N+K)) solution might pass if implemented efficiently.
    # But 5*10^7 in pure Python is risky for 2 seconds.
    #
    # Let's re-evaluate.
    # Is there a way to avoid O(N^2)?
    # The condition for card i (value v) to be unnecessary is:
    # max_subset_sum(<K, All \ {i}) < K - v.
    #
    # Let's consider the sorted array.
    # For a fixed i, the "other" cards are all cards except A[i].
    # To maximize the sum < K, we should greedily take the smallest cards until adding the next one exceeds K.
    # Wait, is it always the smallest cards?
    # Yes! To get the largest sum <= S using a subset of positive integers, you should always pick the smallest numbers first.
    # Why? Because replacing a larger number with a smaller unused number (if available) increases the total sum.
    # So, the strategy to get the max sum < K from a set of positive integers is:
    # Sort the set in ascending order. Take elements from the start until the next element would make the sum >= K.
    # The sum of these elements is the maximum possible sum < K.
    #
    # This simplifies everything immensely!
    # For each card i:
    #   The "other" cards are A without A[i].
    #   Since A is sorted, if we remove A[i], the remaining elements are still sorted (just with a gap).
    #   We iterate from the smallest available elements and sum them up until adding the next smallest would make the sum >= K.
    #   Let this sum be S_i.
    #   Check if S_i < K - A[i].
    #
    # Complexity: O(N^2) because for each of N cards, we might iterate up to N cards.
    # 5000 * 5000 / 2 = 12.5 million iterations. This is very safe for Python.
    
    # Sort A
    sorted_A = sorted(A)
    
    unnecessary_count = 0
    
    # We need to check for each index i in the original array A.
    # But the condition depends on the value.
    # Actually, the problem asks for the number of unnecessary cards.
    # If multiple cards have the same value, we treat them as distinct items.
    # However, since the set of "other" cards is determined by removing one instance, and the greedy strategy
    # works on the multiset of values, the result for a card with value v is the same regardless of which instance of v we remove,
    # provided the multiset of other values is the same.
    # But if we have duplicate values, say two 1s, and we remove the first 1, the set of others has one 1.
    # If we remove the second 1, the set of others has one 1. The set of others is identical.
    # So all cards with the same value will have the same "unnecessary" status.
    # We can just iterate through the sorted array and for each element, simulate the removal.
    # Since N is small, we can just do it for each index in the sorted array, which corresponds to a card.
    # The order in the original array doesn't matter for the count.
    
    for i in range(N):
        # Consider the card with value sorted_A[i].
        # Construct the list of other cards.
        # Since N is 5000, creating a new list each time is O(N), total O(N^2). Acceptable.
        # But to avoid list creation overhead, we can just simulate.
        
        current_sum = 0
        # We iterate through all cards except the one at index i.
        # We want to pick the smallest available ones.
        # Since sorted_A is sorted, we just skip index i.
        
        count = 0
        for j in range(N):
            if j == i:
                continue
            val = sorted_A[j]
            if current_sum + val >= K:
                break
            current_sum += val
            count += 1
        
        # current_sum is the max sum < K using a subset of other cards.
        # Condition for unnecessary: current_sum < K - sorted_A[i]
        if current_sum < K - sorted_A[i]:
            unnecessary_count += 1
            
    print(unnecessary_count)

if __name__ == '__main__':
    solve()