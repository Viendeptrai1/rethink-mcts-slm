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

    # We want to select the maximum number of items such that no two selected items sum to > X.
    # This is equivalent to saying that for every pair in the selected subset, their sum <= X.
    # If we sort the selected subset, it suffices to check that the sum of the two largest elements <= X.
    # To maximize the size of the subset, we should greedily pick the smallest available items.
    # Let the sorted prices be p[0], p[1], ..., p[n-1].
    # We try to pick a prefix of length k: p[0], p[1], ..., p[k-1].
    # The condition is that the two largest, p[k-2] and p[k-1], must satisfy p[k-2] + p[k-1] <= X.
    # However, this logic is slightly flawed if we just take a prefix. Consider if skipping a small number allows us to take more?
    # Actually, if we have a valid set S, and we replace the largest element with a smaller unselected element, the sum of the two largest can only decrease or stay same, so the property is preserved.
    # Therefore, the optimal strategy is always to take the smallest k items.
    # We just need to find the largest k such that the sum of the two largest in the first k items is <= X.
    # Note: if k < 2, the condition is vacuously true (no pairs exist).

    # Let's verify with an example:
    # Prices: 1, 2, 3, 4, 5, X=6
    # k=1: {1} -> valid
    # k=2: {1, 2} -> 1+2=3 <= 6 -> valid
    # k=3: {1, 2, 3} -> 2+3=5 <= 6 -> valid
    # k=4: {1, 2, 3, 4} -> 3+4=7 > 6 -> invalid
    # So max k=3. Matches sample 1.

    # Example 2: 4, 8, 1, 9, 7, X=10
    # Sorted: 1, 4, 7, 8, 9
    # k=1: {1} -> valid
    # k=2: {1, 4} -> 1+4=5 <= 10 -> valid
    # k=3: {1, 4, 7} -> 4+7=11 > 10 -> invalid
    # Max k=2. Matches sample 2.

    # Example 3: 1, 3, 1, 7, X=10
    # Sorted: 1, 1, 3, 7
    # k=1: {1} -> valid
    # k=2: {1, 1} -> 1+1=2 <= 10 -> valid
    # k=3: {1, 1, 3} -> 1+3=4 <= 10 -> valid
    # k=4: {1, 1, 3, 7} -> 3+7=10 <= 10 -> valid (strictly more than X triggers horn, so <= X is safe)
    # Max k=4. Matches sample 3.

    # Algorithm:
    # Iterate k from 1 to n.
    # Check if k >= 2 and prices[k-2] + prices[k-1] > X.
    # If so, stop. The answer is k-1.
    # If loop finishes, answer is n.

    ans = 0
    for k in range(1, n + 1):
        if k >= 2:
            if prices[k-2] + prices[k-1] > X:
                break
        ans = k

    print(ans)

if __name__ == "__main__":
    solve()