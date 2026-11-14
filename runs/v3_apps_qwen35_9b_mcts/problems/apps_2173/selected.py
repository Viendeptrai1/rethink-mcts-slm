import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    a = []
    for i in range(n):
        a.append(int(input_data[i + 1]))

    # Store original indices to restore order later
    indexed_a = [(a[i], i) for i in range(n)]
    # Sort by required rating
    indexed_a.sort(key=lambda x: x[0])

    result = [0] * n
    last_assigned = 0

    for req, original_idx in indexed_a:
        # The rating must be at least 'req' and strictly greater than the previous one
        current_rating = max(req, last_assigned + 1)
        result[original_idx] = current_rating
        last_assigned = current_rating

    # Print the result sequence
    print(*(result))

if __name__ == "__main__":
    solve()