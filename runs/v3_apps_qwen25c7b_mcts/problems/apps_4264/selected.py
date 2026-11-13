def count_odd_digit_numbers(N):
    count = 0
    for i in range(1, N + 1):
        if len(str(i)) % 2 != 0:
            count += 1
    return count

# Example usage:
N = int(input())
print(count_odd_digit_numbers(N))