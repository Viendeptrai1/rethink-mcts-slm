import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    n = int(next(iterator))
    k = int(next(iterator))

    a = []
    for _ in range(n):
        a.append(int(next(iterator)))

    # We need to find the starting index (1-based) that minimizes the total power.
    # The pattern repeats every k tasks. Specifically, if we start at index i (0-based),
    # the tasks Inna catches are at indices: i, i+k, i+2k, ...
    # Since n is divisible by k, there are exactly n/k such tasks for any start offset modulo k.
    # We can compute the sum for each offset from 0 to k-1.

    min_total_power = float('inf')
    best_start_index = -1

    # Calculate sums for each possible starting offset modulo k
    for start_offset in range(k):
        current_sum = 0
        # Iterate through the array with step k, starting from start_offset
        for idx in range(start_offset, n, k):
            current_sum += a[idx]
        
        if current_sum < min_total_power:
            min_total_power = current_sum
            best_start_index = start_offset + 1  # Convert to 1-based index

    print(best_start_index)

if __name__ == "__main__":
    solve()