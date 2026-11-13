import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    k = int(input_data[1])

    # We need exactly k indices i such that p[i] > p[i+1].
    # Strategy:
    # Start with an increasing sequence: 1, 2, 3, ..., n. This has 0 descents.
    # To get k descents, we can reverse a suffix of length k+1.
    # Reversing a contiguous segment [l, r] creates (r - l) descents if the segment was increasing.
    # If we reverse the last k+1 elements (indices n-k to n-1 in 0-based),
    # the number of descents introduced is exactly k.
    # Example: n=5, k=2. Base: 1 2 3 4 5. Reverse last 3 (3,4,5) -> 1 2 5 4 3.
    # Descents: 5>4 (yes), 4>3 (yes). Total 2.
    # Example: n=3, k=0. Reverse last 1 -> no change. 1 2 3. Descents 0.
    # Example: n=3, k=2. Reverse last 3 -> 3 2 1. Descents: 3>2, 2>1 -> 2.

    result = list(range(1, n + 1))
    start_index = n - k - 1
    end_index = n
    result[start_index:end_index] = result[start_index:end_index][::-1]

    print(*(result))

if __name__ == "__main__":
    solve()