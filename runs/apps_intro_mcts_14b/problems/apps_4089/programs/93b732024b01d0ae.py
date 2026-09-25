import sys

def get_dog_name(N):
    # Calculate the length of the name for the dog numbered N
    length = 1
    while True:
        # Number of dogs with names of length 'length'
        num_dogs_with_length = 26 * length
        if N <= num_dogs_with_length:
            break
        N -= num_dogs_with_length
        length += 1
    
    # Convert N to a base-26 number using 'a' to 'z' as digits
    name = []
    for _ in range(length):
        N -= 1  # Adjust for 0-based indexing
        name.append(chr(ord('a') + N % 26))
        N //= 26
    
    return ''.join(reversed(name))

# Read input
N = int(sys.stdin.read().strip())

# Get and print the dog name
print(get_dog_name(N))