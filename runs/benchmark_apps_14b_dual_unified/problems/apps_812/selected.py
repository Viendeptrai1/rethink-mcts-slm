import sys
from collections import defaultdict

def find_index_to_remove(n, b):
    if n == 2:
        return 1
    
    # Count frequency of each element
    freq = defaultdict(int)
    for num in b:
        freq[num] += 1
    
    # Find the most frequent element
    max_freq = max(freq.values())
    most_frequent_elements = [num for num, count in freq.items() if count == max_freq]
    
    # Check if removing any element from the most frequent elements results in an AP
    for j in range(n):
        if b[j] in most_frequent_elements:
            # Create a new list without the j-th element
            new_b = b[:j] + b[j+1:]
            
            # Sort the new list
            new_b.sort()
            
            # Check if the sorted list forms an arithmetic progression
            diff = new_b[1] - new_b[0]
            is_ap = True
            for i in range(2, len(new_b)):
                if new_b[i] - new_b[i-1] != diff:
                    is_ap = False
                    break
            
            if is_ap:
                return j + 1
    
    return -1

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
b = list(map(int, data[1:]))

# Find and print the result
result = find_index_to_remove(n, b)
print(result)