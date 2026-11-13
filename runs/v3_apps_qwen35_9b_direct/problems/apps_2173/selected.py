import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    a = []
    for i in range(n):
        a.append(int(input_data[1 + i]))

    # Store original indices to restore order later
    indexed_a = [(a[i], i) for i in range(n)]

    # Sort by desired rating
    indexed_a.sort(key=lambda x: x[0])

    result = [0] * n
    current = 1

    for val, original_idx in indexed_a:
        if current < val:
            current = val
        result[original_idx] = current
        current += 1

    # Print the result sequence
    print(*(result))

if __name__ == "__main__":
    solve()