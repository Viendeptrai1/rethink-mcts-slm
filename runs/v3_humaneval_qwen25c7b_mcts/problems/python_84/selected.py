def solve(N):
    """Given a positive integer N, return the total sum of its digits in binary."""
    # Calculate the sum of the digits of N
    digit_sum = sum(int(digit) for digit in str(N))
    # Convert the sum to binary and return it as a string
    return bin(digit_sum)[2:]