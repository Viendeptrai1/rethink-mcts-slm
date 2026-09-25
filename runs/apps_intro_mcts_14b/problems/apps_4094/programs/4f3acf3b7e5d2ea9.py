import sys

def find_first_multiple_of_k(K):
    remainder = 0
    length = 0
    
    while True:
        length += 1
        remainder = (remainder * 10 + 7) % K
        if remainder == 0:
            return length

# Read input from standard input
K = int(sys.stdin.read().strip())

# Find and print the position of the first occurrence of a multiple of K
print(find_first_multiple_of_k(K))