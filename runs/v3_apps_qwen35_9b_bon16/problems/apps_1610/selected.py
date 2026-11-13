import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    n = int(data[0])
    k = int(data[1])

    # We need exactly k positions i where p[i] > p[i+1]
    # Strategy: Start with a strictly increasing sequence 1, 2, ..., n (0 descents)
    # Then reverse the first k+1 elements to create k descents at the boundaries between them.
    # Example: n=5, k=2
    # Initial: 1 2 3 4 5 (0 descents)
    # Reverse first k+1 = 3 elements: 3 2 1 4 5
    # Descents: 3>2 (yes), 2>1 (yes), 1>4 (no) -> total 2 descents.
    # This works because reversing an increasing segment of length L creates L-1 descents.
    # We want k descents, so we reverse a segment of length k+1.

    p = list(range(1, n + 1))
    if k > 0:
        # Reverse the first k+1 elements
        end_idx = k  # exclusive index in Python slice (elements 0 to k)
        p[:end_idx + 1] = reversed(p[:end_idx + 1])

    print(*(p))

if __name__ == "__main__":
    solve()