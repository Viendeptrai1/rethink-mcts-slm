def solve(N):
    # Convert the integer N to a string to iterate over each digit
    N_str = str(N)
    
    # Calculate the sum of the digits
    digit_sum = sum(int(digit) for digit in N_str)
    
    # Convert the sum of digits to binary and return it as a string
    return bin(digit_sum)[2:]

# Example usage:
# print(solve(1000))  # Output: "1"
# print(solve(150))   # Output: "110"
# print(solve(147))   # Output: "1100"