def find_marks(n, k, p, x, y, current_marks):
    required_sum = x - sum(current_marks)
    min_median = y
    
    # Calculate the range of possible sums for the remaining tests
    min_possible_sum = sum(current_marks) + k * 1
    max_possible_sum = sum(current_marks) + k * p
    
    if required_sum < min_possible_sum or required_sum > max_possible_sum:
        return -1
    
    # Determine the required range for the middle mark after sorting
    remaining_tests = n - k
    mid_position = remaining_tests // 2
    min_middle_mark = None
    max_middle_mark = None
    
    if mid_position % 2 == 0:
        min_middle_mark = min_median - mid_position // 2
        max_middle_mark = min_median + mid_position // 2
    else:
        min_middle_mark = min_median - mid_position // 2
        max_middle_mark = min_median + mid_position // 2
    
    # Check if it's possible to achieve the required sum with the middle mark range
    for i in range(min_middle_mark, max_middle_mark + 1):
        if required_sum >= k + i * (remaining_tests // 2) and required_sum <= k + i * ((remaining_tests // 2) + 1):
            # Assign marks to satisfy both conditions
            remaining_marks = [i] * remaining_tests
            current_sum = sum(current_marks + remaining_marks)
            current_median = sorted(current_marks + remaining_marks)[(n - 1) // 2]
            
            if current_sum <= x and current_median >= min_median:
                return remaining_marks
    
    return -1

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
p = int(data[2])
x = int(data[3])
y = int(data[4])

current_marks = list(map(int, data[5:]))

# Find and print the result
result = find_marks(n, k, p, x, y, current_marks)
if result == -1:
    print("-1")
else:
    print(" ".join(map(str, result)))