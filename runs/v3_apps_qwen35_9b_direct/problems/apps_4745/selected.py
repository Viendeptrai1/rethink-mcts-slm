import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        X = int(next(iterator))
        prices = []
        for _ in range(n):
            prices.append(int(next(iterator)))
    except StopIteration:
        return

    prices.sort()

    # We want to select a subset S of maximum size such that for any distinct a, b in S:
    # a + b <= X
    #
    # Strategy:
    # If we sort the prices, the condition "any pair sums to <= X" is most restrictive for the two largest elements in the subset.
    # If we pick a subset of size k from the sorted array, to maximize the chance that all pairs sum <= X,
    # we should pick the k smallest elements. Why? Because if the k smallest elements satisfy the condition (max1 + max2 <= X),
    # then any other subset of size k would have elements >= these, so their sums would be even larger.
    #
    # So the problem reduces to: find the largest k such that the sum of the two largest elements in prices[0...k-1] is <= X.
    # The two largest elements in the prefix of length k are prices[k-1] and prices[k-2].
    # We need prices[k-1] + prices[k-2] <= X.
    #
    # Edge case: if k=1, there are no pairs, so the condition is vacuously true. We can always pick at least 1 item (if n>=1).
    # Actually, the problem says "if people buy exactly two...". If we mark only 1 item, no one can buy exactly two, so condition holds.
    # If we mark 0 items, condition holds. But we want max items.
    #
    # Algorithm:
    # 1. Sort prices.
    # 2. Iterate k from n down to 1.
    # 3. Check if the two largest in the first k elements sum <= X.
    #    - If k=1, valid.
    #    - If k>=2, check prices[k-1] + prices[k-2] <= X.
    # 4. The first k (starting from largest) that satisfies this is our answer.
    #
    # Optimization: Since prices are sorted, as k decreases, the sum of the two largest decreases (or stays same).
    # We can start checking from k=n downwards. The first one that works is the answer.
    # Or simpler: iterate k from 1 to n, keep track of the max valid k.
    # Actually, monotonicity: if a subset of size k works, does a subset of size k-1 work?
    # Yes, because the two largest in size k-1 are <= the two largest in size k.
    # So we can binary search or just linear scan. Given n=10^5, linear scan is fine.
    # But we can do it in one pass from the end.

    # Let's try to find the largest k.
    # Start with k = n.
    # While k >= 2 and prices[k-1] + prices[k-2] > X:
    #     k -= 1
    # If k becomes 1, it's valid. If k becomes 0 (only if n=0, but n>=1), handle.
    # Since n>=1, the loop will stop at least at k=1.

    k = n
    while k >= 2:
        if prices[k-1] + prices[k-2] > X:
            k -= 1
        else:
            break

    print(k)

if __name__ == "__main__":
    solve()