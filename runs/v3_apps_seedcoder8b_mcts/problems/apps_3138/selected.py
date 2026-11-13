def count_matching_ranges(n, numbers):
    MOD = 10**9 + 7
    count = 0
    left = 0
    product = 1
    sum_value = 0

    for right in range(n):
        product = (product * numbers[right]) % MOD
        sum_value += numbers[right]

        while left < right and (product > sum_value or product == 0):
            product = (product * pow(numbers[left], MOD - 2, MOD)) % MOD
            sum_value -= numbers[left]
            left += 1

        if left < right and product == sum_value:
            count += 1

    return count

if __name__ == "__main__":
    n = int(input())
    numbers = list(map(int, input().split()))
    result = count_matching_ranges(n, numbers)
    print(result)