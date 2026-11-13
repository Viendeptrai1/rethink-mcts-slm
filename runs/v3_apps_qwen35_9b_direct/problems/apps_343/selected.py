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

    # Current sum
    current_sum = sum(a)
    remaining_tests = n - k
    needed_sum = x - current_sum

    # If even with all 1s we exceed x, impossible
    if needed_sum < remaining_tests:
        print("-1")
        return

    # We need to choose 'remaining_tests' numbers such that:
    # 1. Sum <= x (we will use minimal sum possible to satisfy this, then adjust if needed)
    # 2. Median >= y

    # Strategy:
    # To maximize our chances of satisfying the median constraint while keeping sum low:
    # We should try to set as many numbers as possible to 1 (to keep sum low) 
    # but ensure that at least (n+1)//2 numbers are >= y.
    
    # Let m = (n+1)//2 be the required count of numbers >= y for the median to be >= y.
    m = (n + 1) // 2
    
    # Count how many existing numbers are >= y
    count_ge_y = sum(1 for val in a if val >= y)
    
    # How many more do we need from the remaining tests?
    needed_ge_y = m - count_ge_y
    
    if needed_ge_y < 0:
        needed_ge_y = 0
        
    if needed_ge_y > remaining_tests:
        print("-1")
        return

    # We will assign 'needed_ge_y' numbers to be 'y' (the smallest valid value >= y)
    # and the rest (remaining_tests - needed_ge_y) to be '1' (smallest possible value).
    # This minimizes the sum while satisfying the median constraint.
    
    # Calculate the minimal sum required for the remaining tests
    min_sum_needed = needed_ge_y * y + (remaining_tests - needed_ge_y) * 1
    
    if current_sum + min_sum_needed > x:
        print("-1")
        return

    # Construct the solution
    result = []
    
    # Add the numbers that must be >= y
    for _ in range(needed_ge_y):
        result.append(y)
    
    # Add the rest as 1s
    rest_count = remaining_tests - needed_ge_y
    for _ in range(rest_count):
        result.append(1)
    
    # Output the result
    print(*(result))

if __name__ == "__main__":
    solve()