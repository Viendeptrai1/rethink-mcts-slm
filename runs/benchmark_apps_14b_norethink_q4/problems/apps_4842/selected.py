def find_degree_and_next_value(n, values):
    def calculate_differences(seq):
        return [seq[i+1] - seq[i] for i in range(len(seq) - 1)]

    def find_degree_and_diff(seq):
        diffs = calculate_differences(seq)
        if all(d == diffs[0] for d in diffs):
            return 1, diffs[0]
        else:
            degree, diff = find_degree_and_diff(diffs)
            return degree + 1, diff

    degree, diff = find_degree_and_diff(values)
    last_value = values[-1]
    for _ in range(degree):
        last_value += diff

    return degree, last_value

import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
values = list(map(int, data[1:]))

degree, next_value = find_degree_and_next_value(n, values)
print(degree, next_value)