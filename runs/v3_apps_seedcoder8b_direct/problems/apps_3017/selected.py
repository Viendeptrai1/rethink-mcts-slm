def count_numbers_with_power_of_2(n, e):
    from itertools import product

    # Calculate 2^e and convert it to a string
    power_of_2_str = str(2**e)
    power_of_2_digits = set(power_of_2_str)

    # Function to check if a number contains all digits of power_of_2_str
    def contains_power_of_2_digits(num_str):
        return power_of_2_digits.issubset(set(num_str))

    # Count numbers from 0 to n that contain all digits of 2^e
    count = 0
    for num in range(n + 1):
        if contains_power_of_2_digits(str(num)):
            count += 1

    return count

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip()
    n, e = map(int, data.split())
    result = count_numbers_with_power_of_2(n, e)
    print(result)