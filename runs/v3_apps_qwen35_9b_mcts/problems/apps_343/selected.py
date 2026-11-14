import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    n = int(next(iterator))
    k = int(next(iterator))
    p = int(next(iterator))
    x = int(next(iterator))
    y = int(next(iterator))

    a = []
    for _ in range(k):
        a.append(int(next(iterator)))

    remaining_tests = n - k
    current_sum = sum(a)

    # Sort existing marks to help with median logic
    a.sort()

    # We need the median of the final n elements to be >= y.
    # Since n is odd, the median is at index (n-1)//2 in the sorted final array (0-based).
    # Let m = (n-1)//2. We need at least m+1 elements >= y in the final set.
    # Currently, we have k elements. Let's count how many are >= y.
    count_ge_y = 0
    for val in a:
        if val >= y:
            count_ge_y += 1

    needed_ge_y = (n // 2) + 1 - count_ge_y

    if needed_ge_y > remaining_tests:
        print("-1")
        return

    # Strategy:
    # We need to fill 'remaining_tests' slots.
    # We must put at least 'needed_ge_y' marks equal to y (or higher, but y is optimal for sum).
    # The rest can be 1 (optimal for sum).
    # However, we must ensure that after adding these, the median condition holds.
    # Actually, if we add exactly 'needed_ge_y' marks of value y and the rest 1s,
    # and we place them optimally relative to existing marks, the median will be >= y.
    # Why? Because in the sorted final array, the element at index m (0-based) will be >= y
    # if there are at least m+1 elements >= y. We ensured that count.
    # So the construction is:
    # 1. Take 'needed_ge_y' marks of value y.
    # 2. Take the remaining (remaining_tests - needed_ge_y) marks of value 1.
    # 3. Check if current_sum + (needed_ge_y * y) + (remaining_tests - needed_ge_y) * 1 <= x.
    # If not, it's impossible because we used the minimal possible sum to satisfy the median constraint.

    min_needed_sum = needed_ge_y * y + (remaining_tests - needed_ge_y) * 1
    if current_sum + min_needed_sum > x:
        print("-1")
        return

    # Construct the result
    result = []
    # Add the required y's
    for _ in range(needed_ge_y):
        result.append(y)
    # Add the rest as 1's
    for _ in range(remaining_tests - needed_ge_y):
        result.append(1)

    # Output the result
    print(*(result))

if __name__ == "__main__":
    solve()