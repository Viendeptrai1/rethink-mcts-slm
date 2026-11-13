from collections import defaultdict
import sys

MOD = 998244353

def count_good_permutations(n, s):
    # Separate the pairs into two lists based on their first and second elements
    first_elements = [pair[0] for pair in s]
    second_elements = [pair[1] for pair in s]

    # Count the frequency of each element in both lists
    freq_first = defaultdict(int)
    freq_second = defaultdict(int)
    for elem in first_elements:
        freq_first[elem] += 1
    for elem in second_elements:
        freq_second[elem] += 1

    # Calculate the number of valid permutations
    total_permutations = 1
    for i in range(1, n + 1):
        total_permutations *= (freq_first[i] * freq_second[i])
        total_permutations %= MOD

    return total_permutations

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
s = []
for i in range(n):
    a = int(data[2 * i + 1])
    b = int(data[2 * i + 2])
    s.append((a, b))

# Output the result
print(count_good_permutations(n, s))