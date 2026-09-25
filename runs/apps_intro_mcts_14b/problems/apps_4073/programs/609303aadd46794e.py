import sys

def find_second_largest(n, numbers):
    # Initialize the largest and second largest with very small values
    largest = second_largest = float('-inf')
    
    for number in numbers:
        if number > largest:
            second_largest = largest
            largest = number
        elif number > second_largest and number != largest:
            second_largest = number
    
    return second_largest

# Read input from standard input
input_data = sys.stdin.read().split()
n = int(input_data[0])
numbers = list(map(int, input_data[1:]))

# Find and print the second largest number
print(find_second_largest(n, numbers))