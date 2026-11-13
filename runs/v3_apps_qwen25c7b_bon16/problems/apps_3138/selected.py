def count_matching_ranges(n, pages):
    count = 0
    prefix_sum = [0] * (n + 1)
    prefix_prod = [1] * (n + 1)
    
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + pages[i]
        prefix_prod[i + 1] = prefix_prod[i] * pages[i]
    
    for start in range(n):
        for end in range(start + 1, n):
            if prefix_sum[end + 1] - prefix_sum[start] == prefix_prod[end + 1] // prefix_prod[start]:
                count += 1
    
    return count

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
pages = list(map(int, data[1:]))

# Calculate and print the result
result = count_matching_ranges(n, pages)
print(result)