import sys

def find_divisible_number(n, arr):
    # Initialize the gcd with the first element
    gcd = arr[0]
    
    # Compute the gcd of the entire array
    for i in range(1, n):
        while arr[i] % gcd != 0:
            gcd = arr[i] % gcd
            if gcd == 1:
                return 1
    
    # Check if the gcd is in the array
    if gcd in arr:
        return gcd
    else:
        return -1

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
arr = list(map(int, data[1:]))

# Find and print the result
result = find_divisible_number(n, arr)
print(result)