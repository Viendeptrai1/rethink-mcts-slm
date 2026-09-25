def rounded_avg(n, m):
    if n > m:
        return -1
    total = sum(range(n, m + 1))
    count = m - n + 1
    average = round(total / count)
    return bin(average)

# Example usage:
# print(rounded_avg(1, 5))  # Output: "0b11"
# print(rounded_avg(7, 5))  # Output: -1
# print(rounded_avg(10, 20))  # Output: "0b1111"
# print(rounded_avg(20, 33))  # Output: "0b11010"