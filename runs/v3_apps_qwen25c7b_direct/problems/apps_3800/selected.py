def count_rectangles(a, s):
    n = len(s)
    prefix_sum = [0] * (n + 1)
    for i in range(1, n + 1):
        prefix_sum[i] = prefix_sum[i - 1] + int(s[i - 1])
    
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            total = 0
            for k in range(j, n):
                total += (prefix_sum[k + 1] - prefix_sum[i]) * (k - j + 1)
                if total == a:
                    count += 1
    
    return count

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
a = int(data[0])
s = data[1]
print(count_rectangles(a, s))