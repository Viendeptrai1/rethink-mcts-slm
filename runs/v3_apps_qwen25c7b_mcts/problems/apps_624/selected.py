def max_average_power(n, k, m, powers):
    powers.sort()
    operations = m
    for i in range(n):
        if operations > 0 and powers[i] < powers[-1]:
            increase = min(k, operations)
            powers[i] += increase
            operations -= increase
    return sum(powers) / n

# Example usage:
# n, k, m = map(int, input().split())
# powers = list(map(int, input().split()))
# result = max_average_power(n, k, m, powers)
# print(result)