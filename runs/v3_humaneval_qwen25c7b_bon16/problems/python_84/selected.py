def solve(N):
    # Convert the number to a string to iterate over each digit
    num_str = str(N)
    # Sum the digits
    digit_sum = sum(int(digit) for digit in num_str)
    # Convert the sum to binary and remove the '0b' prefix
    binary_result = bin(digit_sum)[2:]
    return binary_result