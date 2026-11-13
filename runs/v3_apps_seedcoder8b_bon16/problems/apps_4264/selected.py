def count_odd_digit_numbers(N):
    def count_digits(n):
        return len(str(n))
    
    count = sum(1 for i in range(1, N + 1) if count_digits(i) % 2 != 0)
    return count

N = int(input())
result = count_odd_digit_numbers(N)
print(result)