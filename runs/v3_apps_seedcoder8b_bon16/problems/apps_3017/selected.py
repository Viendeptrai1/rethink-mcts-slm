def count_numbers_with_power_of_2_digits(n, e):
    import itertools
    
    # Calculate the power of 2
    power_of_2 = 2 ** e
    power_of_2_str = str(power_of_2)
    
    # Calculate the length of the power of 2 string
    power_of_2_length = len(power_of_2_str)
    
    # Function to check if a number contains the digits of power_of_2 as a substring
    def contains_power_of_2_digits(number_str):
        # Generate all substrings of the given number of the same length as power_of_2
        for i in range(len(number_str) - power_of_2_length + 1):
            substring = number_str[i:i + power_of_2_length]
            if substring == power_of_2_str:
                return True
        return False
    
    count = 0
    
    # Iterate through all numbers from 0 to n
    for num in range(n + 1):
        num_str = str(num)
        if contains_power_of_2_digits(num_str):
            count += 1
    
    return count

# Read input from standard input
import sys
input = sys.stdin.read
data = input().strip()
n, e = map(int, data.split())

# Call the function and print the result
print(count_numbers_with_power_of_2_digits(n, e))