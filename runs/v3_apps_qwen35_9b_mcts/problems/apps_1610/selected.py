import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    k = int(input_data[1])

    # We need exactly k descents where p[i] > p[i+1].
    # Strategy:
    # Place the first k elements in descending order: n, n-1, ..., n-k+1
    # Then place the remaining n-k elements in ascending order: 1, 2, ..., n-k
    # This creates exactly k descents at the boundaries between the two segments.
    # Note: The last element of the first segment is (n-k+1) and the first of the second is 1.
    # Since n-k+1 > 1 (because k < n), there is a descent at the junction.
    # Within the first segment, every adjacent pair is a descent (k-1 descents).
    # Within the second segment, there are no descents.
    # Total descents = (k-1) + 1 = k.

    result = []
    # First part: descending from n down to n-k+1
    for i in range(k):
        result.append(n - i)
    
    # Second part: ascending from 1 up to n-k
    for i in range(1, n - k + 1):
        result.append(i)

    print(*(result))

if __name__ == "__main__":
    solve()