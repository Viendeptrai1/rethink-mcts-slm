import sys

def max_participants(n, k, preferences):
    # Create a list to store the groups
    groups = [0] * (n + 1)
    
    # Assign each participant to their group
    for i in range(1, n + 1):
        groups[i] = preferences[i - 1]
    
    # Create a dictionary to count the size of each group
    group_size = {}
    
    # Traverse the groups and count the size of each group
    for i in range(1, n + 1):
        if i not in group_size:
            size = 0
            current = i
            while True:
                size += 1
                current = groups[current]
                if current == i:
                    break
            group_size[i] = size
    
    # Sort the groups by size in descending order
    sorted_groups = sorted(group_size.items(), key=lambda x: x[1], reverse=True)
    
    # Select the largest groups until the bus capacity is reached
    selected = 0
    for group, size in sorted_groups:
        if k >= size:
            k -= size
            selected += size
        else:
            break
    
    return selected

# Read input from stdin
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
preferences = list(map(int, data[2:]))

# Print the result
print(max_participants(n, k, preferences))