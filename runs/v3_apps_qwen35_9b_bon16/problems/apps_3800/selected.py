import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    a = int(input_data[0])
    s = input_data[1]
    n = len(s)

    # Convert string to list of integers
    digits = [int(c) for c in s]

    # If a is 0, we need to count rectangles where sum of products is 0.
    # The sum of b_ij in a rectangle is sum(i in x..y) sum(j in z..t) (s[i] * s[j])
    # = (sum(s[i] for i in x..y)) * (sum(s[j] for j in z..t))
    # Let S1 = sum of digits in row range, S2 = sum of digits in col range.
    # We need S1 * S2 = a.

    # Precompute prefix sums of digits to quickly calculate range sums
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i+1] = pref[i] + digits[i]

    # Function to get sum of digits from index i to j (inclusive, 0-based)
    def get_row_sum(i, j):
        return pref[j+1] - pref[i]

    # We need to find number of pairs of ranges (row_range, col_range) such that
    # (sum of digits in row_range) * (sum of digits in col_range) = a

    # If a == 0:
    # Either sum(row_range) == 0 or sum(col_range) == 0 (or both).
    # Number of ways = (count of row ranges with sum 0) * (total col ranges) + 
    #                  (count of col ranges with sum 0) * (total row ranges) - 
    #                  (count of row ranges with sum 0) * (count of col ranges with sum 0)
    # Because the intersection (both zero) is counted twice.
    
    # If a != 0:
    # We need sum(row_range) * sum(col_range) = a.
    # Iterate over all possible values of S1 (sum of a row range), find how many row ranges give S1.
    # Then for each S1, we need S2 = a / S1. If a % S1 == 0, then we need S2 = a // S1.
    # Count how many col ranges give S2, multiply counts, and sum up.

    total_ranges = n * (n + 1) // 2

    # Count frequencies of all possible range sums
    # Since digits are 0-9 and n <= 4000, max sum is 9*4000 = 36000.
    # We can use a frequency array or dictionary.
    
    from collections import Counter

    sum_counts = Counter()
    
    # Enumerate all ranges
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += digits[j]
            sum_counts[current_sum] += 1

    if a == 0:
        # Count ranges with sum 0
        count_zero = sum_counts[0]
        # Total pairs where product is 0:
        # Case 1: row sum is 0, col sum is anything -> count_zero * total_ranges
        # Case 2: col sum is 0, row sum is anything -> total_ranges * count_zero
        # Intersection: row sum 0 AND col sum 0 -> count_zero * count_zero
        # Result = count_zero * total_ranges + total_ranges * count_zero - count_zero * count_zero
        #        = 2 * count_zero * total_ranges - count_zero * count_zero
        ans = 2 * count_zero * total_ranges - count_zero * count_zero
        print(ans)
    else:
        ans = 0
        # Iterate over possible sums S1
        for s1, cnt1 in sum_counts.items():
            if s1 == 0:
                continue
            if a % s1 != 0:
                continue
            s2 = a // s1
            # Check if s2 exists in sum_counts
            if s2 in sum_counts:
                cnt2 = sum_counts[s2]
                ans += cnt1 * cnt2
        print(ans)

if __name__ == '__main__':
    solve()