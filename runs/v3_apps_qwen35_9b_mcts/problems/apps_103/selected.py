import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    a = []
    for i in range(n):
        a.append(int(input_data[1 + i]))

    max_erased = 0

    # Try erasing a consecutive segment from index i to j (inclusive)
    # The segment length is j - i + 1
    for i in range(n):
        for j in range(i, n):
            length = j - i + 1
            if length == 0:
                continue

            # Determine the lower bound for the missing segment
            if i == 0:
                lower_bound = 1
            else:
                lower_bound = a[i - 1] + 1

            # Determine the upper bound for the missing segment
            if j == n - 1:
                upper_bound = 1000
            else:
                upper_bound = a[j + 1] - 1

            # The number of available integers in the range [lower_bound, upper_bound]
            available_count = max(0, upper_bound - lower_bound + 1)

            # To uniquely restore the array, the number of erased elements must equal
            # the number of available integers in the gap.
            if available_count == length:
                if length > max_erased:
                    max_erased = length

    print(max_erased)

if __name__ == "__main__":
    solve()