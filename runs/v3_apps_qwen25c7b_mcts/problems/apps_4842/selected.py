def find_polynomial_degree_and_next_value(n, values):
    def calculate_differences(values):
        return [values[i] - values[i - 1] for i in range(1, len(values))]

    differences = values[:]
    degree = 0

    while len(set(differences)) > 1:
        differences = calculate_differences(differences)
        degree += 1

    next_value = values[-1] + differences[0]
    return degree, next_value

import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
values = list(map(int, data[1:]))

degree, next_value = find_polynomial_degree_and_next_value(n, values)
print(degree, next_value)