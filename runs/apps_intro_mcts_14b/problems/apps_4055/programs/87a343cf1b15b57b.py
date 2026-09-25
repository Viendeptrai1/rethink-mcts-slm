import sys

def min_lights_to_turn_off(n, a):
    k = 0
    i = 1
    while i < n - 1:
        if a[i - 1] == 1 and a[i] == 0 and a[i + 1] == 1:
            # Found a disturbed flat at position i
            k += 1
            # Skip the next flat as turning off the current one resolves it
            i += 2
        else:
            i += 1
    return k

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:]))

# Calculate and print the result
result = min_lights_to_turn_off(n, a)
print(result)