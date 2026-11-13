from collections import defaultdict

def count_matching_ranges(n, numbers):
    prefix_sum = [0] * (n + 1)
    prefix_product = [1] * (n + 1)
    
    for i in range(1, n + 1):
        prefix_sum[i] = prefix_sum[i - 1] + numbers[i - 1]
        prefix_product[i] = prefix_product[i - 1] * numbers[i - 1]
    
    count = 0
    sum_map = defaultdict(int)
    product_map = defaultdict(int)
    
    for i in range(2, n + 1):
        if prefix_sum[i] - prefix_sum[0] == prefix_product[i] - prefix_product[0]:
            count += 1
        
        if prefix_sum[i] in sum_map:
            count += sum_map[prefix_sum[i]]
        
        if prefix_product[i] in product_map:
            count += product_map[prefix_product[i]]
        
        sum_map[prefix_sum[i]] += 1
        product_map[prefix_product[i]] += 1
    
    return count

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
numbers = list(map(int, data[1:]))

print(count_matching_ranges(n, numbers))