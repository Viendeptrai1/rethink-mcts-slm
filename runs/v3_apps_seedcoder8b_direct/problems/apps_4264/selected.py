def count_odd_digit_numbers(N):
    def count_digits(x):
        return len(str(x))
    
    odd_digit_count = 0
    for i in range(1, N + 1):
        if count_digits(i) % 2 != 0:
            odd_digit_count += 1
    
    return odd_digit_count

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    N = int(input().strip())
    print(count_odd_digit_numbers(N))