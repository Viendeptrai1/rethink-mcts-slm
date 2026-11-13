def count_numbers_with_power_of_2_digits(n, e):
    power_of_2 = str(2**e)
    power_length = len(power_of_2)
    count = 0

    for k in range(n + 1):
        k_str = str(k)
        if power_of_2 in k_str:
            count += 1

    return count

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip()
    n, e = map(int, data.split())
    result = count_numbers_with_power_of_2_digits(n, e)
    print(result)