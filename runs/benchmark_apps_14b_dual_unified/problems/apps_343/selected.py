def find_marks(n, k, p, x, y, a):
    remaining_tests = n - k
    current_sum = sum(a)
    current_median = sorted(a)[k // 2]
    
    # Check if it's possible to achieve the desired result
    if current_sum + remaining_tests * p < x or current_median < y:
        return "-1"
    
    # Initialize the result array with the minimum possible marks
    result = [y] * remaining_tests
    
    # Adjust the result to meet the sum constraint
    while current_sum + sum(result) > x:
        for i in range(remaining_tests):
            if result[i] < p:
                result[i] += 1
                break
        else:
            return "-1"
    
    # Ensure the median constraint is met
    combined = sorted(a + result)
    median = combined[n // 2]
    if median < y:
        return "-1"
    
    return " ".join(map(str, result))

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
p = int(data[2])
x = int(data[3])
y = int(data[4])
a = list(map(int, data[5:]))

# Output the result
print(find_marks(n, k, p, x, y, a))