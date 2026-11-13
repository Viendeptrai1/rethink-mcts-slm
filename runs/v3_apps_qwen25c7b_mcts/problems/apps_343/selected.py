def find_marks(n, k, p, x, y, marks):
    current_sum = sum(marks)
    current_median = sorted(marks)[(n - 1) // 2]
    
    if current_sum > x or current_median < y:
        return -1
    
    remaining_tests = n - k
    remaining_sum_needed = x - current_sum
    remaining_median_needed = y
    
    for i in range(k, n):
        max_mark = min(p, remaining_sum_needed // remaining_tests)
        if max_mark >= remaining_median_needed:
            marks.append(max_mark)
            remaining_sum_needed -= max_mark
            remaining_tests -= 1
        else:
            break
    
    if remaining_tests > 0:
        return -1
    
    return marks[k:]

# Example usage:
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
p = int(data[2])
x = int(data[3])
y = int(data[4])
marks = list(map(int, data[5:]))

result = find_marks(n, k, p, x, y, marks)
if result == -1:
    print(-1)
else:
    print(" ".join(map(str, result)))