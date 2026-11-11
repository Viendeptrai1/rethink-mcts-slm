import sys

def count_odd_digit_numbers(N):
    count = 0
    for i in range(1, N + 1):
        if len(str(i)) % 2 == 1:
            count += 1
    return count

if __name__ == "__main__":
    N = int(sys.stdin.read().strip())
    result = count_odd_digit_numbers(N)
    print(result)