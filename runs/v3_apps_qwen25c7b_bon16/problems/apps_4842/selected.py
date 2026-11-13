def find_next_value_and_degree(values):
    def calculate_differences(lst):
        return [lst[i] - lst[i-1] for i in range(1, len(lst))]

    differences = values[:]
    degree = 0

    while len(set(differences)) != 1:
        differences = calculate_differences(differences)
        degree += 1

    next_value = values[-1] + differences[0]
    return degree, next_value

import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
values = list(map(int, data[1:]))

degree, next_value = find_next_value_and_degree(values)
print(degree, next_value)